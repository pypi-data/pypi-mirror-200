# #ifdef SERVER
import multiprocessing
import time
import xmlrpc.client
import sys
from pathlib import Path

import pytest

from testmon_dev.process_code import methods_to_checksums
from testmon_dev.testmon_core import collect_mhashes
from tests.lib4tests import DirectTransportPlugin, DirectTransport
from tmserver.database import ServerDatabase
from tmserver.wiring import GunicornTestmonApp
from tests.test_core import CoreTestmonDataForTest, FINGERPRINT1, DEFAULT_DURATION

pytest_plugins = ("pytester",)


@pytest.fixture()
def free_port():
    """
    https://gist.github.com/bertjwregeer/0be94ced48383a42e70c3d9fff1f4ad0
    """

    def _find_free_port():
        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", 0))
        portnum = s.getsockname()[1]
        s.close()

        return portnum

    return _find_free_port()


def rpc_server_init_and_serve(port=8236):
    print("starting server_database at port ", port)
    GunicornTestmonApp({"bind": f"localhost:{port}"}).run()


@pytest.fixture
def http_server(free_port):
    process = multiprocessing.Process(
        target=rpc_server_init_and_serve, args=(free_port,)
    )
    print("initiating server_database ")
    process.start()
    time.sleep(0.3)

    yield

    process.terminate()
    process.join()


@pytest.fixture
def xmlrpc_proxy(testdir):
    return xmlrpc.client.ServerProxy(
        f"http://dummy:1", DirectTransport(), allow_none=True
    )


@pytest.fixture
def http_proxy(testdir, http_server, free_port):
    print("instantiating serverproxy at port ", free_port)
    rpc_proxy = xmlrpc.client.ServerProxy(
        f"http://localhost:{free_port}/test", allow_none=True
    )
    for i in range(10):
        try:
            rpc_proxy.fetch_attribute("nonexistent")
            break
        except ConnectionRefusedError:
            time.sleep(0.1)

    return rpc_proxy


@pytest.fixture
def http_tmdata(http_proxy):
    yield CoreTestmonDataForTest(database=http_proxy)


@pytest.fixture
def directory_with_git_history(testdir):
    # if the field suite_run.version.git_sha and gitlog match, testmon doesn't reach out to the network before
    # running the tests
    testdir.run("git", "init", ".")
    testdir.chdir("dir")


class TestInjectDirectTransport:
    def test_assumptions(self, testdir, xmlrpc_proxy):
        testdir.makepyfile(
            test_a="""
                    def test_1():
                        pass
                   """
        )
        testdir.runpytest_inprocess(
            "--tmnet-dev", "-v", plugins=[DirectTransportPlugin()]
        )
        assert (
            len(ServerDatabase(".serverdbs/test.db").all_test_executions(exec_id=1))
            == 1
        )

    def test_simple_change(self, testdir, xmlrpc_proxy):
        testdir.makepyfile(
            test_a="""
            def test_add():
                assert 1 + 2 == 3

            def test_2():
                assert True
                    """
        )

        result = testdir.runpytest_inprocess(
            "--tmnet-dev", "-vv", plugins=[DirectTransportPlugin()]
        )
        result.stdout.fnmatch_lines(
            [
                "*2 passed*",
            ]
        )

        test_a = testdir.makepyfile(
            test_a="""
            def test_add():
                assert 1 + 2 + 3 == 6

            def test_2():
                assert True
                    """
        )
        test_a.setmtime(1424880935)

        result = testdir.runpytest_inprocess(
            "--tmnet-dev",
            "--testmon-dev-nocollect",
            "-vv",
            plugins=[DirectTransportPlugin()],
        )
        result.stdout.fnmatch_lines(
            [
                "*1 passed, 1 deselected*",
            ]
        )


class TestServerMethods:
    def test_initiate_execution(self, xmlrpc_proxy: ServerDatabase):
        result = xmlrpc_proxy.initiate_execution(
            "test",  # environment_name,
            "3.11.0",  # python_version, # TODO
            "build==0.9.0;click==8.1.3;coverage==6.5.0",  # system_packages
            # local db sha is behind the repo (server_database might have more data)
        )
        assert result["exec_id"] == 1
        assert result["filenames"] == []

    @pytest.mark.skip(reason="not implemented yet")  # TODO
    def test_download(self, xmlrpc_proxy):
        ret_value = xmlrpc_proxy.initiate_execution(
            1,
            "lksdjfo9jflskdjf",
            "test",
            "3.11",
            "build==0.9.0;click==8.1.3;coverage==6.5.0",
            "3104c24\ndf84a21\n2ac9b1c",
            "df84a21",
            1,
            # local db sha is behind the repo (server_database might have more data)
        )
        print(ret_value)
        # ... continue execution as normal

    def test_upload_only(self, xmlrpc_proxy: ServerDatabase):
        result = xmlrpc_proxy.initiate_execution(
            "default",
            "build==0.9.0;click==8.1.3;coverage==6.5.0",
            "3.11",
        )

        records = []
        for filename in {"test_a.py"}:
            records.append(
                {
                    "method_checksums": FINGERPRINT1,
                    "filename": filename,
                    "mtime": 1.0,
                    "checksum": "100",
                }
            )

        xmlrpc_proxy.insert_test_file_fps(
            {"test_a.py::test_1": {"deps": records}}, result["exec_id"]
        )

    @pytest.mark.skip(reason="not implemented yet")  # TODO
    def test_decide_recency_locally(self, directory_with_git_history):
        directory_with_githistory.runpytest_inprocess("--testmon")
        testmon.is_recent()
        directory_with_githistory

    def test_matching(self, xmlrpc_proxy: ServerDatabase, testdir):
        exec_id = self.new_exec(xmlrpc_proxy)

        xmlrpc_proxy.insert_test_file_fps(
            dict(
                easy_fixture("test_1", {"test_a.py": 1, "a.py": 2})
                + easy_fixture("test_2", {"test_a.py": 1, "a.py": 2})
                + easy_fixture("test_3", {"test_a.py": 1, "a2.py": 4})
                + easy_fixture("test_4", {"test_b.py": 3, "b.py": 5})
            ),
            exec_id,
        )

        exec_id = self.new_exec(xmlrpc_proxy)

        result = xmlrpc_proxy.fetch_unknown_files(
            {"test_a.py": 1, "a.py": 2, "b.py": 5, "a2.py": 4, "test_b.py": 100},
            exec_id,
        )
        assert result == ["test_b.py"]

        exec_id = self.new_exec(xmlrpc_proxy)

        result = xmlrpc_proxy.fetch_unknown_files(
            {"test_a.py": 1, "a.py": 2, "test_b.py": 3, "b.py": 4}, exec_id
        )
        assert result == [
            "a2.py",
            "b.py",
        ]

    def new_exec(self, xmlrpc_proxy):
        result = xmlrpc_proxy.initiate_execution(
            "default",
            "3.11",
            "build==0.9.0;click==8.1.3;coverage==6.5.0",
        )
        exec_id = result["exec_id"]
        return exec_id

    def test_new_determine_stable_flow(self, xmlrpc_proxy):
        td = CoreTestmonDataForTest(database=xmlrpc_proxy)
        td.write_fixture("test_1.py::test_1", {"test_1.py": FINGERPRINT1})
        del td.source_tree.cache["test_1.py"]

        filenames = td.db.filenames(td.exec_id)

        assert filenames == ["test_1.py"]

        assert (
            len(
                td.db.fetch_unknown_files(
                    {"test_1.py": "100"},
                    td.exec_id,
                )
            )
            == 0
        )
        changed_file_data = td.db.fetch_unknown_files({"test_1.py": "101"}, td.exec_id)

        assert changed_file_data == ["test_1.py"]

        files_mhashes = collect_mhashes(td.source_tree, changed_file_data)

        misses = td.db.determine_tests(td.exec_id, files_mhashes)["affected"]

        assert misses == ["test_1.py::test_1"]


DEFAULT_M_CHECKSUMS = [0]


class AddableDict(dict):
    def __add__(self, other):
        return AddableDict({**self, **other})


def easy_fixture(test, f_checksums=None, method_checksums=None):
    if method_checksums is None:
        method_checksums = {}
    records = []
    for filename in f_checksums:
        full_test_name = f"{filename}::{test}"
        break

    for filename, f_checksum in f_checksums.items():
        records.append(
            {
                "method_checksums": method_checksums.get(filename, DEFAULT_M_CHECKSUMS),
                "filename": filename,
                "checksum": f_checksums.get(
                    filename, method_checksums.get(filename, DEFAULT_M_CHECKSUMS)
                ),
            }
        )
    return AddableDict({full_test_name: {"deps": records}})


class TestClientServerIntegration:
    def test_write_read_nodedata_remote(self, xmlrpc_proxy):
        result = xmlrpc_proxy.initiate_execution(
            "default",
            "build==0.9.0;click==8.1.3;coverage==6.5.0",
            "3.11",
        )

        testmon_data_with_http_proxy = CoreTestmonDataForTest(database=xmlrpc_proxy)

        testmon_data_with_http_proxy.write_fixture(
            "test_a.py", {"test_a.py": FINGERPRINT1}
        )

        assert testmon_data_with_http_proxy.all_files == ["test_a.py"]


class TestViaHttp:
    @pytest.mark.skipif(sys.platform == "win32", reason="Windows platform")
    def test_initiate_execution(self, http_tmdata: ServerDatabase, http_proxy):
        ret_value = http_proxy.initiate_execution(
            "default",  # environment_name,
            "build==0.9.0;click==8.1.3;coverage==6.5.0",  # system_packages,
            "3.11",  # python_version,
        )
        assert ret_value
        assert Path(".serverdbs/test.db").exists()

    @pytest.mark.skip
    def test_write_read_nodedata_remote(self, http_proxy):
        testmon_data_with_http_proxy = CoreTestmonDataForTest(database=http_proxy)
        testmon_data_with_http_proxy.write_fixture("test_a.py::n1")

    def test_basic(self, testdir, http_proxy, free_port):
        testdir.makeini(
            f"""
            [pytest]
            testmon_dev_url = http://localhost:{free_port}/
            testmon_dev_api_key = test_af654g54eb7c
            """
        )
        testdir.makepyfile(
            test_a="""
                    def test_1():
                        pass
                   """
        )
        testdir.runpytest_subprocess("--tmnet-dev")
        assert (
            len(
                ServerDatabase(datafile=".serverdbs/test.db").all_test_executions(
                    exec_id=1
                )
            )
            == 1
        )

    def test_many_insert_test_file_fps(self, http_tmdata: ServerDatabase, http_proxy):
        http_proxy.initiate_execution(
            "default",  # environment_name,
            "build==0.9.0;click==8.1.3;coverage==6.5.0",  # system_packages,
            "3.11",  # python_version,
        )

        test_file_fps = {}
        for filename in [str(x) for x in range(10)]:
            for test in [str(x) for x in range(10)]:
                test_file_fps[f"{filename}::{test}"] = {
                    "deps": [
                        {
                            "method_checksums": methods_to_checksums(["0match"]),
                            "filename": filename,
                            "checksum": "100",
                        }
                    ]
                }
        http_tmdata.save_test_execution_file_fps(test_file_fps)


class TestServerDatabase:
    def test_write_read_client_and_server(self, testdir, xmlrpc_proxy):
        tmdata = CoreTestmonDataForTest(database=xmlrpc_proxy)
        tmdata.write_fixture("test_a.py::test_n1", {"test_a.py": FINGERPRINT1})
        server_data = ServerDatabase(".serverdbs/test.db")

        assert tmdata.db.all_test_executions(tmdata.exec_id)
        assert tmdata.db.all_test_executions(
            tmdata.exec_id
        ) == server_data.all_test_executions(1)


# #endif
