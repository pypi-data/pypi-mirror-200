# #ifdef SERVER
# pylint: disable-all
import itertools
import logging
import os
import platform
import re
import sentry_sdk
import sys
import traceback

from sentry_sdk import capture_exception, configure_scope
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware
from timeit import default_timer as timer
from xmlrpc.server import SimpleXMLRPCDispatcher
from xmlrpc.client import loads, dumps, Fault

if platform.system() != "Windows":
    from gunicorn.app.base import BaseApplication
else:

    class BaseApplication:
        def __init__(self):
            raise NotImplemented("Windows doesn't support gunicorn servers")


from tmserver.database import ServerDatabase

control_chars = bytes(itertools.chain(range(0x00, 0x20), range(0x7F, 0xA0)))
control_char_re = re.compile(b"[" + control_chars + b"]")

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", None),
    traces_sample_rate=1.0,
    send_default_pii=True,
    _experiments={
        "profiles_sample_rate": 1.0,
    },
)


def remove_control_chars(input_string):
    return control_char_re.sub(b"", input_string)


logger = logging.getLogger(__name__)

DISPATCHER_PARAMS = {"allow_none": True, "encoding": None}


class TestmonRPCWsgi:
    def __init__(self, dbdir=".serverdbs"):

        self.dbdir = dbdir

        self._dispatchers = {}

    def _get_dispatcher(self, name):
        if name in self._dispatchers:
            return self._dispatchers[name]

        dispatcher = SimpleXMLRPCDispatcher(**DISPATCHER_PARAMS)
        dispatcher.register_instance(ServerDatabase(datafile=f"{self.dbdir}/{name}.db"))
        dispatcher.register_multicall_functions()

        self._dispatchers[name] = dispatcher

        return dispatcher

    def _testmon_marshaled_dispatch(self, data, project):
        """Taken from SimpleXMLRPCDispatcher"""
        dispatcher = self._get_dispatcher(project)
        try:
            start_time = timer()

            print(f"{project}: processing {len(data)}, ", end=" ")

            params, method = loads(
                remove_control_chars(data),
            )
            print(f"{method}  ({timer() - start_time}) ..", end=" ")
            with configure_scope() as scope:
                scope.set_transaction_name(method)
                scope.set_extra("method", method)

            response = (dispatcher._dispatch(method, params),)

            response = dumps(response, methodresponse=1, **DISPATCHER_PARAMS)
        except Fault as fault:
            print(f"{fault} when processing:\n{data}")
            capture_exception(fault)
            response = dumps(fault, **DISPATCHER_PARAMS)
        except Exception as e:
            traceback_string = traceback.format_exc()
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(f"{traceback_string} when processing:\n{data}")
            capture_exception(e)
            try:
                response = dumps(
                    Fault(1, f"{exc_type}:{exc_value}"),
                    **DISPATCHER_PARAMS,
                )
            finally:
                exc_type = exc_value = exc_tb = None
        print(f"finished in {timer() - start_time}")
        return response.encode(dispatcher.encoding, "xmlcharrefreplace")

    def __call__(self, environ, start_response):
        project = environ["PATH_INFO"].split("/")[1]
        with configure_scope() as scope:
            scope.set_extra("project", project)
        try:
            if not environ["REQUEST_METHOD"] == "POST":
                start_response("400 Bad Request", (("Content-Type", "text/plain"),))
                return ()

            length = int(environ["CONTENT_LENGTH"])
            data = environ["wsgi.input"].read(length)
            with configure_scope() as scope:
                scope.set_extra("data", data)

            response = self._testmon_marshaled_dispatch(data, project)

            start_response(
                "200 OK",
                (
                    ("Content-Type", "text/xml"),
                    ("Content-Length", str(len(response))),
                ),
            )

            return [bytes(response)]
        except Exception as e:  # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            logger.exception(e)
            capture_exception(e)
            start_response("500 Server error", [("Content-Type", "text/plain")])
            return []


class GunicornTestmonApp(BaseApplication):
    def __init__(self, options=None):
        self.options = options or {}
        self.application = TestmonRPCWsgi(options.get("db_dir", ".serverdbs"))
        super().__init__()

    def init(self, *args, **kwargs):
        raise NotImplementedError

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    main_options = {
        "bind": "0.0.0.0:8080",
        "workers": 1,
        "loglevel": "INFO",
        "db_dir": "/var/data/.serverdbs",
        "timeout": "57",
    }
    gta = GunicornTestmonApp(main_options)
    gta.application = SentryWsgiMiddleware(gta.application)
    gta.run()

# #endif
