import pytest

from testmon_dev.configure import TmConf
from testmon_dev import configure


class TestConfigure:
    @pytest.fixture()
    def options(self):
        return {
            "testmon-dev": False,
            "testmon-dev_noselect": False,
            "testmon-dev_nocollect": False,
            "testmon-dev_forceselect": False,
            "no-testmon-dev": False,
            "keyword": "",
            "markexpr": "",
            "lf": False,
            "file_or_dir": [],
        }

    def test_easy(self, options):
        options["testmon-dev"] = True
        assert configure._header_collect_select(options) == TmConf(
            "testmon-dev: ",
            True,
            True,
        )

    def test_empty(self, options):
        options["testmon-dev"] = None
        assert configure._header_collect_select(options) == TmConf(None, False, False)

    def test_dogfooding(self, options):
        options["testmon-dev"] = True
        assert configure._header_collect_select(
            options, dogfooding=True, debugger=True
        ) == TmConf("testmon-dev: ", True, True)

    def test_noselect(self, options):
        options["testmon-dev_noselect"] = True
        assert configure._header_collect_select(options) == TmConf(
            "testmon-dev: selection deactivated, ",
            True,
            False,
        )

    def test_noselect_trace(self, options):
        options["testmon-dev_noselect"] = True
        assert configure._header_collect_select(options, debugger=True) == TmConf(
            (
                "testmon-dev: collection automatically deactivated because "
                "it's not compatible with debugger, selection deactivated, "
            ),
            False,
            False,
        )

    def test_nocollect_minus_k(self, options):
        options["keyword"] = "test1"
        options["testmon-dev_nocollect"] = True
        assert configure._header_collect_select(options) == TmConf(
            (
                "testmon-dev: collection deactivated, "
                "selection automatically deactivated because -k was used, "
            ),
            False,
            False,
        )

    def test_nocollect_coverage(self, options):  # duplicate lower
        options["testmon-dev"] = True
        assert configure._header_collect_select(options, coverage=True) == (
            (
                "testmon-dev: collection automatically deactivated "
                "because coverage.py was detected and simultaneous collection is not supported, "
            ),
            False,
            True,
        )

    # whatchout, duplicate name test_nocollect_coverage
    # #ifdef PYTEST_COV
    def test_nocollect_coverage(self, options):  # noqa: F811
        options["testmon-dev"] = True
        assert configure._header_collect_select(
            options, coverage=True, cov_plugin=True
        ) == TmConf("testmon-dev: ", True, True)

    # #endif
