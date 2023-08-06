import os

import datetime
from typing import Callable

import pkg_resources
import sys
import textwrap
import time
import pytest

from testmon_dev import db
from testmon_dev.process_code import (
    Module,
    create_fingerprint_source,
    create_fingerprint,
)
from testmon_dev.testmon_core import (
    eval_environment,
    DB_FILENAME,
    TestmonData,
)
from testmon_dev.process_code import blob_to_checksums

from testmon_dev.testmon_core import TestmonCollector as CoreTestmon
from testmon_dev.testmon_core import TestmonData as CoreTestmonData
from tests.test_process_code import CodeSample
from tests.coveragepy import coveragetest
from tests.test_core import CoreTestmonDataForTest

from threading import Thread, Condition

# #ifdef SERVER
from tests.lib4tests import DirectTransportPlugin

# #endif
from tests.lib4tests import GetTestmonDataPlugin

pytest_plugins = ("pytester",)

datafilename = os.environ.get("TESTMON_DATAFILE", DB_FILENAME)


def two_lines_function():
    a = 1
    return a + 1


def track_it(testdir, func):
    testmon = CoreTestmon(rootdir=testdir.tmpdir.strpath, testmon_labels=set())
    testmon_data = CoreTestmonData("")
    #    testmon.setup_coverage()
    testmon.start_testmon("test_a.py::test_1")
    func()
    nodes_files_lines = testmon.get_batch_coverage_data()
    testmon.close()

    files_fingerprints = {}
    for filename, lines in nodes_files_lines["test_a.py::test_1"].items():
        module = testmon_data.source_tree.get_file(filename)
        if module:
            fingerprint = create_fingerprint(module, lines)
            files_fingerprints[filename] = fingerprint

    return files_fingerprints


@pytest.fixture
def test_a(testdir):
    return testdir.makepyfile(
        test_a="""\
                def test_1():
                    print(1)
    """
    )


def changepyfile(testdir, *args, **kwargs):
    f = testdir.makepyfile(*args, **kwargs)
    f.setmtime(1)
    return f


def write_source_code_to_a_file(file_handle, source_code):
    file_handle.write_text(textwrap.dedent(source_code), "utf-8")
    return file_handle


def tm_flavors():
    try:
        from tests.lib4tests import DirectTransportPlugin

        return ("local", "remote")
    except ImportError:
        return ("local",)


class LocalRemote:
    def __init__(
        self,
        testdir: pytest.Testdir = None,
        runpytest_inprocess: Callable = None,
        makepyfile: Callable = None,
        name: str = None,
        mkpydir: Callable = None,
        td: TestmonData = None,
        tmpdir=None,
    ):
        self.testdir = testdir
        self.runpytest_inprocess = runpytest_inprocess
        self.makepyfile = makepyfile
        self.name = name
        self.mkpydir = mkpydir
        self.td = td
        self.tmpdir = tmpdir


def remote_runpytest_gen(lr, testdir):
    def remote_runpytest_inprocess(*args, **kwargs):
        if kwargs:
            raise NotImplemented()
        dtp = DirectTransportPlugin()
        gtd = GetTestmonDataPlugin()
        result = testdir.runpytest_inprocess(*args, **{"plugins": [dtp, gtd]})
        lr.td = gtd.testmon_data
        return result

    return remote_runpytest_inprocess


def lri_gen(lr, testdir):
    def local_runpytest_inprocess(*args, **kwargs):
        if kwargs:
            raise NotImplemented()
        gtd = GetTestmonDataPlugin()
        result = testdir.runpytest_inprocess(*args, **{"plugins": [gtd]})
        lr.td = gtd.testmon_data
        return result

    return local_runpytest_inprocess


@pytest.fixture
def local_remote(request, testdir) -> LocalRemote:
    if request.param == "remote":
        remote = LocalRemote(
            testdir,
            None,
            testdir.makepyfile,
            "remote",
            testdir.mkpydir,
            None,
            testdir.tmpdir,
        )

        remote.runpytest_inprocess = remote_runpytest_gen(remote, testdir)

        return remote

    if request.param == "local":
        lr = LocalRemote(
            testdir,
            None,
            testdir.makepyfile,
            "local",
            testdir.mkpydir,
            None,
            testdir.tmpdir,
        )

        lr.runpytest_inprocess = lri_gen(lr, testdir)

        return lr


class TestCoreTestmon:
    def test_start_stop(self):
        testmon = CoreTestmon("")
        testmon.start_testmon("1")
        testmon2 = CoreTestmon("")
        testmon2.start_testmon("2")
        testmon3 = CoreTestmon("")
        testmon3.close()
        testmon2.start_testmon("4")
        two_lines_function()
        testmon2.close()
        testmon.close()


class TestFundamental:
    @pytest.mark.xfail
    def test_changed_constants_module(self, testdir):
        testdir.makepyfile(
            consts="""
            A = 1
        """
        )
        testdir.makepyfile(
            test_a="""
            import consts
            def test_add():
                assert consts.A == 1
        """
        )
        testdir.runpytest_inprocess("--testmon-dev")
        changepyfile(
            testdir,
            consts="""
            A = 2
        """,
        )
        result = testdir.runpytest_inprocess("--testmon-dev")
        result.reprec.assertoutcome(failed=1)


class TestPytestReportHeader:
    def test_nocollect(self, testdir, test_a):
        result = testdir.runpytest_inprocess("--testmon-dev-nocollect")
        result.stdout.fnmatch_lines(
            [
                "*testmon-dev: collection deactivated*",
            ]
        )

    def test_help(self, testdir, test_a):
        result = testdir.runpytest_inprocess("--testmon-dev", "--help")
        assert result.ret == 0

    def test_select(self, testdir, test_a):
        result = testdir.runpytest_inprocess("--testmon-dev-noselect")
        result.stdout.fnmatch_lines(
            [
                "*testmon-dev: selection deactivated*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_survey_notification(self, local_remote):
        match_string = (
            "We'd like to hear from testmon users! "
            "🙏🙏 go to https://testmon.org/survey to leave feedback ✅❌"
        )
        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines([match_string])

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.no_fnmatch_line(match_string)

        tmdata = local_remote.td

        tmdata.db.write_attribute(
            "last_survey_notification_date",
            str(datetime.date.today() - datetime.timedelta(days=30)),
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines([match_string])
        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.no_fnmatch_line(match_string)

    def test_no(self, testdir, test_a):
        result = testdir.runpytest_inprocess("--no-testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*testmon-dev: deactivated through --no-testmon-dev*",
            ]
        )

    @pytest.mark.xfail  # TODO fix
    def test_deactivated_bc_coverage(self, testdir, test_a):
        result = testdir.run("coverage", "run", "-m", "pytest", "--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*testmon-dev: collection automatically deactivated "
                "because coverage.py was detected and simultaneous collection is not supported*"
            ]
        )

    def test_active_newdb(self, testdir, test_a):
        result = testdir.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*testmon-dev: new DB, environment: default",
            ]
        )

    def test_active_deselect(self, testdir, test_a):
        testdir.runpytest_inprocess("--testmon-dev")
        result = testdir.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*testmon-dev: changed files: 0, unchanged files: 1*",
            ]
        )

    def test_nocollect_deselect(self, testdir, test_a):
        testdir.runpytest_inprocess("--testmon-dev")
        result = testdir.runpytest_inprocess("--testmon-dev-nocollect")
        result.stdout.fnmatch_lines(
            [
                "*testmon-dev: collection deactivated, changed files: 0, "
                "unchanged files: 1*",
            ]
        )


FINGERPRINTPRINT = create_fingerprint_source("print(1)", {1})


class TestVariant:
    def test_separation(self, testdir):
        td1 = CoreTestmonDataForTest(environment="1")
        td1.write_fixture("test_a.py::test_1", {"test_a.py": FINGERPRINTPRINT})

        td2 = CoreTestmonDataForTest(environment="2")
        td2.write_fixture("test_a.py::test_2", {"test_a.py": FINGERPRINTPRINT})

        td3 = CoreTestmonData(
            "",
            environment="2",
        )
        assert set(td3.all_tests) == {"test_a.py::test_2"}

    def test_header(self, testdir):
        testdir.makeini(
            """
                        [pytest]
                        environment_expression='1'
                        """
        )
        result = testdir.runpytest_inprocess("-v", "--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*testmon-dev: new DB, environment: 1*",
            ]
        )

    def test_header_nonstr(self, testdir):
        testdir.makeini(
            """
                        [pytest]
                        environment_expression=int(1)
                        """
        )
        result = testdir.runpytest_inprocess("-v", "--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*testmon-dev: new DB, environment: 1*",
            ]
        )

    def test_empty(self, testdir):
        config = testdir.parseconfigure()
        assert eval_environment(config.getini("environment_expression")) == ""

    def test_environment_md5(self, testdir, monkeypatch):
        testdir.makeini(
            """
                        [pytest]
                        environment_expression=md5('TEST')
                        """
        )
        config = testdir.parseconfigure()
        assert (
            eval_environment(config.getini("environment_expression"))
            == "033bd94b1168d7e4f0d644c3c95e35bf"
        )

    def test_env(self, testdir, monkeypatch):
        monkeypatch.setenv("TEST_V", "JUST_A_TEST")
        testdir.makeini(
            """
                        [pytest]
                        environment_expression=os.environ.get('TEST_V')
                        """
        )
        config = testdir.parseconfigure()
        assert (
            eval_environment(config.getini("environment_expression")) == "JUST_A_TEST"
        )

    def test_nonsense(self, testdir):
        testdir.makeini(
            """
                        [pytest]
                        environment_expression=nonsense
                        """
        )
        config = testdir.parseconfigure()
        assert "NameError" in eval_environment(config.getini("environment_expression"))

    # Test that ``os`` is available in list comprehensions.
    def test_complex(self, testdir, monkeypatch):
        monkeypatch.setenv("TEST_V", "JUST_A_TEST")
        testdir.makeini(
            """
            [pytest]
            environment_expression="_".join([x + ":" + os.environ[x] for x in os.environ if x == 'TEST_V'])
            """  # noqa: E501
        )
        config = testdir.parseconfigure()
        assert (
            eval_environment(config.getini("environment_expression"))
            == "TEST_V:JUST_A_TEST"
        )


class TestmonDeselect(object):
    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_dont_readcoveragerc(self, local_remote):
        p = local_remote.tmpdir.join(".coveragerc")
        p.write("[")
        local_remote.makepyfile(
            test_a="""
            def test_add():
                pass
        """
        )
        local_remote.runpytest_inprocess("--testmon-dev")

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_simple_change(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            def test_add():
                assert 1 + 2 == 3
                    """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

        test_a = local_remote.makepyfile(
            test_a="""
            def test_add():
                assert 1 + 2 + 3 == 6
                    """
        )
        test_a.setmtime(1424880935)

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*passed*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_status_code_tests_deselected(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            def test_add():
                assert 1 == 1
                    """
        )

        # running testmon with one passed test
        local_remote.runpytest_inprocess("--testmon-dev")

        # running testmon with one deselected test
        result = local_remote.runpytest_inprocess("--testmon-dev")
        assert result.ret == 0

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_simple_change_1_of_2(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            def test_add():
                assert 1 + 2 == 3

            def test_2():
                assert True
                    """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*2 passed*",
            ]
        )

        test_a = local_remote.makepyfile(
            test_a="""
            def test_add():
                assert 1 + 2 + 3 == 6

            def test_2():
                assert True

                    """
        )
        test_a.setmtime(1424880935)

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*1 passed, 1 deselected*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_re_executing_failed(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            import os

            def test_file(): # test that on first run fails, but on second one passes
                if os.path.exists('check'): # if file exists then pass the test
                    assert True
                else: # otherwise create the file and fail the test
                    open('check', 'a').close()
                    assert False
                    """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*1 failed*",
            ]
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*no tests ran*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_simple_change_1_of_2_with_decorator(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            import pytest

            @pytest.mark.skipif('False')
            def test_add():
                assert 1 + 2 == 3

            def test_2():
                assert True
                    """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*2 passed*",
            ]
        )

        time.sleep(0.1)
        local_remote.makepyfile(
            test_a="""
            import pytest

            @pytest.mark.skipif('False')
            def test_add():
                assert 1 + 2 + 3 == 6

            def test_2():
                assert True
                    """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*1 passed, 1 deselected*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_not_running_after_failure(self, local_remote):
        tf = local_remote.makepyfile(
            test_a="""
            def test_add():
                pass
        """,
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.assert_outcomes(1, 0, 0)

        sys.modules.pop("test_a", None)

        tf = local_remote.makepyfile(
            test_a="""
            def test_add():
                1/0
        """,
        )
        tf.setmtime(1424880936)
        result = local_remote.runpytest_inprocess("--testmon-dev", "-v")
        result.assert_outcomes(0, 0, 1)
        sys.modules.pop("test_a", None)

        tf = local_remote.makepyfile(
            test_a="""
            def test_add():
                blas
        """,
        )
        tf.setmtime(1424880937)
        result = local_remote.runpytest_inprocess("--testmon-dev", "-v")
        result.assert_outcomes(0, 0, 1)

        sys.modules.pop("test_a", None)

        tf = local_remote.makepyfile(
            test_a="""
            def test_add():
                pass
                pass
        """,
        )
        tf.setmtime(1424880938)
        result = local_remote.runpytest_inprocess("--testmon-dev", "-v")
        result.assert_outcomes(1, 0, 0)
        sys.modules.pop("test_a", None)

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_fantom_failure(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            def test_add():
                1/0
        """,
        )
        local_remote.runpytest_inprocess("--testmon-dev", "-v")

        tf = local_remote.makepyfile(
            test_a="""
            def test_add():
                pass
        """,
        )
        tf.setmtime(1)
        local_remote.runpytest_inprocess("--testmon-dev", "-v")

        result = local_remote.runpytest_inprocess("--testmon-dev", "-v")
        result.assert_outcomes(0, 0, 0)

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_skipped(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            import pytest
            @pytest.mark.skip
            def test_add():
                1/0
        """,
        )
        local_remote.runpytest_inprocess("--testmon-dev", "-v")
        testmon_data = local_remote.td
        assert "test_a.py::test_add" in testmon_data.all_tests

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_skipped_starting_line2(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            #line not in AST
            import pytest
            @pytest.mark.skip
            def test_add():
                1/0
        """,
        )
        local_remote.runpytest_inprocess("--testmon-dev", "-v")
        assert "test_a.py::test_add" in local_remote.td.all_tests

    @pytest.mark.xfail
    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_skipped_under_dir(self, local_remote):
        subdir = local_remote.testdir.mkdir("tests")

        tf = subdir.join("test_a.py")
        tf.write(
            textwrap.dedent(
                """
            import pytest
            @pytest.mark.skip
            def test_add():
                1/0
        """,
            )
        )
        tf.setmtime(1)
        local_remote.runpytest_inprocess("--testmon-dev", "-v", "tests")

        testmon_data = local_remote.td

        assert "tests/test_a.py" + "::test_add" in testmon_data.all_tests
        assert "tests/test_a.py" in testmon_data.all_files

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_wrong_result_processing(self, local_remote):
        def assert_test_failed(test_name, testmon_data):
            result = testmon_data.all_tests[test_name]["failed"]
            return result

        tf = local_remote.makepyfile(
            test_a="""
            def test_add():
                1/0
        """,
        )

        configs = []

        local_remote.runpytest_inprocess(
            "--testmon-dev",
            "-v",
        )

        assert assert_test_failed("test_a.py::test_add", local_remote.td)

        tf = local_remote.makepyfile(
            test_a="""
            import pytest
            @pytest.mark.skip
            def test_add():
                1/0/0
        """,
        )
        tf.setmtime(1)
        local_remote.runpytest_inprocess(
            "--testmon-dev",
            "-v",
        )

        assert assert_test_failed("test_a.py::test_add", local_remote.td) == False

        tf = local_remote.makepyfile(
            test_a="""
            import pytest
            def test_add():
                1/0
        """,
        )
        tf.setmtime(2)
        local_remote.runpytest_inprocess(
            "--testmon-dev",
            "-v",
        )

        assert assert_test_failed("test_a.py::test_add", local_remote.td)

    def test_lf(self, testdir):
        testdir.makepyfile(
            test_a="""
            def test_add():
                1/0
        """,
        )
        testdir.runpytest_inprocess("--testmon-dev", "-v")

        result = testdir.runpytest_inprocess("--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*1 failed*",
            ]
        )

        result = testdir.runpytest_inprocess("--testmon-dev", "-v", "--lf")
        result.stdout.fnmatch_lines(
            [
                "*selection automatically deactivated because --lf was used*",
                "*1 failed in*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_easy(self, local_remote):
        expected_paths = {"source/a.py", "testing/test_a.py"}

        tests_subdir_path = local_remote.mkpydir("testing")
        source_subdir_path = local_remote.mkpydir("source")
        testfile = tests_subdir_path / "test_a.py"
        testfile.write_text(
            """from source.a import add
def test_add():    assert add(1, 2) == 3
            """,
            encoding="utf-8",
        )
        sourcefile = source_subdir_path / "a.py"
        sourcefile.write_text(
            """def add(a, b):    return a + b
            """,
            encoding="utf-8",
        )
        result = local_remote.runpytest_inprocess("--testmon-dev", "--tb=long", "-v")
        result.stdout.fnmatch_lines(
            [
                "*test_a.py::test_add PASSED*",
            ]
        )
        testmon_data = local_remote.td

        testmon_data.all_files = set(testmon_data.db.filenames(testmon_data.exec_id))
        testmon_data.determine_stable()
        assert testmon_data.all_files == expected_paths, testmon_data.all_files
        assert testmon_data.unstable_files == set()
        assert testmon_data.stable_files == expected_paths, testmon_data.stable_files
        assert not bool(testmon_data.system_packages_change)

    def test_packages_hit(self, testdir):
        testdir.makepyfile(
            test_a="""
            def test_add():
                assert True
        """
        )
        testdir.runpytest_inprocess("--testmon-dev")

        tmdata_with_dummy_packages = CoreTestmonData("")
        tmdata_with_dummy_packages.determine_stable()

        assert tmdata_with_dummy_packages.stable_files == {"test_a.py"}
        assert bool(not tmdata_with_dummy_packages.system_packages_change)
        tmdata_with_dummy_packages.close_connection()

    def test_packages_miss(self, testdir):
        testdir.makepyfile(
            test_a="""
            def test_add():
                assert True
        """
        )
        testdir.runpytest_inprocess("--testmon-dev")

        tmdata_with_dummy_packages = CoreTestmonData("", system_packages="nonsense")

        tmdata_with_dummy_packages.determine_stable()

        assert bool(tmdata_with_dummy_packages.system_packages_change)
        tmdata_with_dummy_packages.close_connection()

    def test_interrupted(self, test_a, testdir):
        testdir.runpytest_inprocess("--testmon-dev")

        tf = testdir.makepyfile(
            test_a="""
            def test_1():
                raise KeyboardInterrupt
         """
        )
        os.utime(datafilename, (1800000000, 1800000000))
        tf.setmtime(1800000000)

        testdir.runpytest_subprocess(
            "--testmon-dev",
        )

        # interrupted run shouldn't save .testmondata
        assert 1800000000 == os.path.getmtime(datafilename)

    @pytest.mark.xfail  # TODO save more often than every 100 tests.
    def test_interrupted_xdist(self, test_a, testdir):
        tf2 = testdir.makeconftest(
            """
            import pytest

            @pytest.hookimpl
            def pytest_configure(config):
                global plugin_config
                plugin_config = config


            @pytest.hookimpl
            def pytest_runtest_logreport(report):
                if not hasattr(plugin_config, "workerinput") and report.nodeid.endswith("test_6"):
                    raise KeyboardInterrupt
         """
        )

        tf = testdir.makepyfile(
            test_a="""
            import time
            def test_1():
                a = 1

            def test_2():
                a = 1

            def test_3():
                a = 1

            def test_3():
                a = 1

            def test_4():
                a = 1

            def test_5():
                time.sleep(2)

            def test_6():
                a = 1

            def test_7():
                a = 1

         """
        )
        result = testdir.runpytest_subprocess("--testmon-dev", "-n1", "-v")
        testmon_data = CoreTestmonData()
        testmon_data.determine_stable()
        assert "test_a.py::test_1" not in testmon_data.unstable_test_names
        assert "test_a.py::test_8" in testmon_data.unstable_test_names
        assert result.ret == 2, result

    def test_interrupted01(self, testdir):
        testdir.makepyfile(
            test_a="""
                import time
                def test_1():
                    pass

                def test_2():
                    time.sleep(0.1)

                def test_3():
                    time.sleep(0.15)
        """
        )
        testdir.runpytest_inprocess("--testmon-dev")

        testdir.makepyfile(
            test_a="""
                import time
                def test_1():
                    time.sleep(0.015)

                def test_2():
                    raise KeyboardInterrupt

                def test_3():
                    time.sleep(0.035)
         """
        )
        td = CoreTestmonData("")
        td.determine_stable()
        assert td.unstable_test_names == {
            "test_a.py::test_1",
            "test_a.py::test_2",
            "test_a.py::test_3",
        }

        result = testdir.runpytest_subprocess("--testmon-dev", "-v")
        result.stdout.no_fnmatch_line("*test_a.py::test_2 PASSED*")

        td.determine_stable()
        assert td.unstable_test_names == {"test_a.py::test_2", "test_a.py::test_3"}

    def test_interrupted_chdir(self, testdir):
        testdir.makepyfile(
            test_a="""
                import time
                def test_1():
                    pass

                def test_2():
                    time.sleep(0.1)

                def test_3():
                    time.sleep(0.15)
        """
        )
        testdir.runpytest_inprocess("--testmon-dev")

        testdir.makepyfile(
            test_a="""
                pytest_plugins = ('pytester',)
                import time
                def test_1():
                    time.sleep(0.015)

                def test_2(testdir):
                    raise KeyboardInterrupt

                def test_3():
                    time.sleep(0.035)
         """
        )

        try:
            testdir.runpytest_inprocess("--testmon-dev", "-v")
        except KeyboardInterrupt:
            pass

        testdir.makepyfile(
            test_a="""
                pytest_plugins = ('pytester',)
                import time
                def test_1():
                    time.sleep(0.016)

         """
        )
        result = testdir.runpytest_inprocess("--testmon-dev", "-v")
        result.stdout.fnmatch_lines("*test_a.py::test_1 PASSED*")

    def test_interrupted_teardown(self, testdir):
        testdir.makepyfile(
            test_a="""
                import time
                import pytest

                @pytest.fixture
                def fixture():
                    yield

                def test_1():
                    pass

                def test_2(fixture):
                    time.sleep(0.1)

                def test_3():
                    time.sleep(0.15)
        """
        )
        testdir.runpytest_inprocess("--testmon-dev")

        testdir.makepyfile(
            test_a="""
                import time
                import pytest

                @pytest.fixture
                def fixture():
                    yield
                    raise KeyboardInterrupt

                def test_1():
                    time.sleep(0.015)

                def test_2(fixture):
                    time.sleep(0.025)

                def test_3():
                    time.sleep(0.035)
         """
        )
        td = CoreTestmonData("")

        td.determine_stable()
        assert td.unstable_test_names == {
            "test_a.py::test_1",
            "test_a.py::test_2",
            "test_a.py::test_3",
        }

        testdir.runpytest_subprocess("--testmon-dev")

        td.determine_stable()
        assert td.unstable_test_names == {"test_a.py::test_2", "test_a.py::test_3"}

    def test_outcomes_exit(self, test_a, testdir):
        testdir.runpytest_inprocess("--testmon-dev")

        tf = testdir.makepyfile(
            test_a="""
             def test_1():
                 import pytest
                 pytest.exit("pytest_exit")
         """
        )
        os.utime(datafilename, (1800000000, 1800000000))
        tf.setmtime(1800000000)
        testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        # interrupted run shouldn't save .testmondata
        assert 1800000000 == os.path.getmtime(datafilename)

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_nonfunc_class(self, local_remote, monkeypatch):
        cs1 = CodeSample(
            """\
            class TestA(object):
                def test_one(self):
                    print("1")

                def test_two(self):
                    print("2")
        """
        )

        cs2 = CodeSample(
            """\
            class TestA(object):
                def test_one(self):
                    print("1")

                def test_twob(self):
                    print("2")
        """
        )
        Module(cs2.source_code)

        test_a = local_remote.makepyfile(test_a=cs1.source_code)
        result = local_remote.runpytest_inprocess(
            "--testmon-dev", "test_a.py::TestA::test_one"
        )
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

        local_remote.makepyfile(test_a=cs2.source_code)
        test_a.setmtime(1424880935)
        result = local_remote.runpytest_inprocess("-v", "--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*2 passed*",
            ]
        )

    def test_strange_argparse_handling(self, testdir):
        cs1 = CodeSample(
            """\
            class TestA(object):
                def test_one(self):
                    print("1")

                def test_two(self):
                    print("2")
        """
        )

        testdir.makepyfile(test_a=cs1.source_code)
        result = testdir.runpytest_inprocess(
            "-v", "--testmon-dev", "test_a.py::TestA::test_one"
        )
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

    def test_nonfunc_class_2(self, testdir):
        testdir.parseconfigure()
        cs2 = CodeSample(
            """\
            class TestA(object):
                def test_one(self):
                    print("1")

                def test_twob(self):
                    print("2")
        """
        )
        testdir.makepyfile(test_a=cs2.source_code)

        result = testdir.runpytest_inprocess(
            "-vv",
            "--collectonly",
            "--testmon-dev",
        )
        result.stdout.fnmatch_lines(
            [
                "*test_one*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_new(self, local_remote):
        a = local_remote.makepyfile(
            a="""
            def add(a, b):
                a = a
                return a + b

            def subtract(a, b):
                return a - b
        """
        )

        local_remote.makepyfile(
            b="""
            def divide(a, b):
                return a // b

            def multiply(a, b):
                return a * b
        """
        )

        local_remote.makepyfile(
            test_a="""
            from a import add, subtract
            import time

            def test_add():
                assert add(1, 2) == 3

            def test_subtract():
                assert subtract(1, 2) == -1
                    """
        )

        local_remote.makepyfile(
            test_b="""
            import unittest

            from b import multiply, divide

            class TestB(unittest.TestCase):
                def test_multiply(self):
                    self.assertEqual(multiply(1, 2), 2)

                def test_divide(self):
                    self.assertEqual(divide(1, 2), 0)
        """
        )
        local_remote.makepyfile(
            test_ab="""
            from a import add
            from b import multiply
            def test_add_and_multiply():
                assert add(2, 3) == 5
                assert multiply(2, 3) == 6
        """
        )
        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*5 passed*",
            ]
        )
        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*collected 0 items*",
            ]
        )
        a.setmtime(1424880935)
        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*no tests ran*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_new_subdir(self, local_remote):
        src_a = """
            def add(a, b):
                a = a
                return a + b

            def subtract(a, b):
                return a - b
        """

        src_b = """
            def divide(a, b):
                return a // b

            def multiply(a, b):
                return a * b
        """
        src_test_a = """
            from source.a import add, subtract
            import time

            def test_add():
                assert add(1, 2) == 3

            def test_subtract():
                assert subtract(1, 2) == -1
                    """

        src_test_b = """
            import unittest

            from source.b import multiply, divide

            class TestB(unittest.TestCase):
                def test_multiply(self):
                    self.assertEqual(multiply(1, 2), 2)

                def test_divide(self):
                    self.assertEqual(divide(1, 2), 0)
        """
        src_test_ab = """
            from source.a import add
            from source.b import multiply
            def test_add_and_multiply():
                assert add(2, 3) == 5
                assert multiply(2, 3) == 6
        """

        source_subdir_path = local_remote.mkpydir("source")
        tests_subdir_path = local_remote.mkpydir("testing")

        a = write_source_code_to_a_file(source_subdir_path / "a.py", src_a)
        write_source_code_to_a_file(source_subdir_path / "b.py", src_b)
        write_source_code_to_a_file(tests_subdir_path / "test_a.py", src_test_a)
        write_source_code_to_a_file(tests_subdir_path / "test_b.py", src_test_b)
        write_source_code_to_a_file(tests_subdir_path / "test_ab.py", src_test_ab)

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*5 passed*",
            ]
        )
        result = local_remote.runpytest_inprocess("--testmon-dev")

        result.stdout.fnmatch_lines(
            [
                "*collected 0 items*",
            ]
        )
        a.setmtime(1424880935)
        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*no tests ran*",
            ]
        )

    def test_different_subdirs_execution(self, testdir):
        testdir.run("touch", "pytest.ini")
        src_a = """
            def add(a, b):
                a = a
                return a + b

            def subtract(a, b):
                return a - b
        """

        src_b = """
            def divide(a, b):
                return a // b

            def multiply(a, b):
                return a * b
        """
        src_test_a = """
            import sys
            sys.path.append('..')
            from source.a import add, subtract
            import time

            def test_add():
                assert add(1, 2) == 3

            def test_subtract():
                assert subtract(1, 2) == -1
                    """

        src_test_b = """
            from source.b import multiply, divide

            class TestB:
                def test_multiply(self):
                    assert multiply(1, 2) ==  2

                def test_divide(self):
                    assert divide(1, 2) == 0
        """
        src_test_ab = """
            from source.a import add
            from source.b import multiply
            def test_add_and_multiply():
                assert add(2, 3) == 5
                assert multiply(2, 3) == 6
        """

        source_subdir_path = testdir.mkpydir("source")
        tests_subdir_path = testdir.mkdir("tests")

        a = write_source_code_to_a_file(source_subdir_path / "a.py", src_a)
        write_source_code_to_a_file(source_subdir_path / "b.py", src_b)
        write_source_code_to_a_file(tests_subdir_path / "test_a.py", src_test_a)
        write_source_code_to_a_file(tests_subdir_path / "test_b.py", src_test_b)
        write_source_code_to_a_file(tests_subdir_path / "test_ab.py", src_test_ab)

        result = testdir.runpytest_inprocess("--testmon-dev", syspathinsert=True)
        result.stdout.fnmatch_lines(
            [
                "*5 passed*",
            ]
        )
        result = testdir.runpytest_inprocess("--testmon-dev", syspathinsert=True)

        result.stdout.fnmatch_lines(
            [
                "*collected 0 items*",
            ]
        )
        a.setmtime(1424880935)
        os.chdir(tests_subdir_path)
        result = testdir.run(
            "pytest", "--testmon-dev", "-c", "../pytest.ini", "--rootdir=.."
        )
        result.stdout.fnmatch_lines(
            [
                "*no tests ran*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_remove_lib(self, local_remote):
        lib = local_remote.makepyfile(
            lib="""
            def a():
                return 1
        """
        )

        local_remote.makepyfile(
            test_a="""
            try:
                from lib import a
            except:
                pass

            def test_a():
                assert a() == 1
            """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.assert_outcomes(1, 0, 0)
        time.sleep(0.01)
        lib.remove()
        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.assert_outcomes(0, 0, 1)

    def test_newr(self, testdir):
        a = testdir.makepyfile(
            a="""
            def add(a, b):
                a = a
                return a + b

            def subtract(a, b):
                return a - b
        """
        )

        testdir.makepyfile(
            b="""
            def divide(a, b):
                return a // b

            def multiply(a, b):
                return a * b
        """
        )

        testdir.makepyfile(
            a_test="""
            from a import add, subtract
            import time

            def test_add():
                assert add(1, 2) == 3

            def test_subtract():
                assert subtract(1, 2) == -1
                    """
        )

        testdir.makepyfile(
            b_test="""
            import unittest

            from b import multiply, divide

            class TestB(unittest.TestCase):
                def test_multiply(self):
                    self.assertEqual(multiply(1, 2), 2)

                def test_divide(self):
                    self.assertEqual(divide(1, 2), 0)
        """
        )

        testdir.makepyfile(
            ab_test="""
            from a import add
            from b import multiply
            def test_add_and_multiply():
                assert add(2, 3) == 5
                assert multiply(2, 3) == 6
        """
        )
        result = testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        result.stdout.fnmatch_lines(
            [
                "*5 passed*",
            ]
        )
        result = testdir.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*collected 0 items*",
            ]
        )
        a.setmtime(1424880935)
        result = testdir.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*no tests ran*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_new2(self, local_remote):
        a = local_remote.makepyfile(
            a="""
            def add(a, b):
                return a + b
        """
        )

        local_remote.makepyfile(
            test_a="""
            from a import add

            def test_add():
                assert add(1, 2) == 3
                    """
        )

        result = local_remote.runpytest_inprocess(
            "--testmon-dev",
        )
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

        a = local_remote.makepyfile(
            a="""
            def add(a, b):
                return a + b + 0
        """
        )
        a.setmtime(1424880935)
        result = local_remote.runpytest_inprocess(
            "--testmon-dev",
        )
        result.stdout.fnmatch_lines(
            [
                "*passed*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_zero_lines_touched(self, local_remote):
        local_remote.makepyfile(
            test_c="""
            import unittest

            class TestA(unittest.TestCase):
                @unittest.skip('')
                def test_add(self):
                    pass
        """
        )
        result = local_remote.runpytest_inprocess(
            "--testmon-dev",
        )
        result.stdout.fnmatch_lines(
            [
                "*1 skipped*",
            ]
        )

    @pytest.mark.xfail(
        sys.platform == "win32", reason="handle of a subprocess is not released"
    )
    def test_changed_data_version(self, testdir, monkeypatch):
        testdir.makepyfile(
            test_pass="""
            def test_pass():
                pass
        """
        )
        result = testdir.runpytest_inprocess("--testmon-dev")
        assert result.ret == 0

        # Now change the data version and check py.test then refuses to run
        monkeypatch.setattr(db, "DATA_VERSION", db.DATA_VERSION + 1)
        result = testdir.runpytest_inprocess("--testmon-dev")

        result.stdout.fnmatch_lines(
            [
                ("*new DB*"),
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_dependent_testmodule(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            def test_1():
                pass
        """
        )
        local_remote.makepyfile(
            test_b="""
            import test_a
            def test_2():
                pass
        """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        assert result.ret == 0

        local_remote.makepyfile(
            test_b="""
            import test_a
            def test_2():
                pass
                pass
        """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        assert result.ret == 0
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

    def test_track_pytest_equal(self, testdir, monkeypatch):
        a = testdir.makepyfile(
            test_a="""\
                        def test_1():
                            a=1
                    """
        )

        def func():
            testdir.runpytest_inprocess("test_a.py")

        deps = track_it(testdir, func)
        assert (
            {
                os.path.relpath(
                    a.strpath, testdir.tmpdir.strpath
                ): create_fingerprint_source(
                    """\
                                def test_1():
                                    a=1
                            """,
                    {1, 2},
                )
            }
            == deps
        )

    def test_run_dissapearing(self, testdir):
        a = testdir.makepyfile(
            test_a="""\
            import sys
            import os
            with open('b73003.py', 'w') as f:
                f.write("print('printing from b73003.py')")
            sys.path.append('.')
            import b73003
            os.remove('b73003.py')
        """
        )

        def f():
            coveragetest.import_local_file("test_a")

        deps = track_it(testdir, f)
        assert os.path.relpath(a.strpath, testdir.tmpdir.strpath) in deps
        assert len(deps) == 1

    def test_report_roundtrip(self, testdir):
        class PlugRereport:
            def pytest_runtest_protocol(self, item, nextitem):
                getattr(item.ihook, "pytest_runtest_logreport")
                # hook(report=)
                return True

        testdir.makepyfile(
            """
        def test_a():
            raise Exception('exception from test_a')
        """
        )

        result = testdir.runpytest_inprocess(
            "-s",
            "-v",
            plugins=[PlugRereport()],
        )

        result.stdout.fnmatch_lines(
            [
                "*no tests ran*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_dependent_testmodule2(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            def test_1():
                pass
        """
        )
        local_remote.makepyfile(
            test_b="""
            import test_a
            def test_2():
                pass
        """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        assert result.ret == 0

        local_remote.makepyfile(
            test_b="""
            import test_a
            def test_2():
                pass
                pass
        """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        assert result.ret == 0
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_dependent_testmodule2_subdir(self, local_remote):
        tests_subdir_path = local_remote.mkpydir("subdir")

        src_test_a = """
            def test_1():
                pass
        """

        local_remote.makepyfile(
            test_b="""
                    import subdir.test_a
                    def test_2():
                        pass
                """
        )

        write_source_code_to_a_file(tests_subdir_path / "test_a.py", src_test_a)

        result = local_remote.runpytest_inprocess("--testmon-dev")
        assert result.ret == 0

        local_remote.makepyfile(
            test_b="""
            import subdir.test_a
            def test_2():
                pass
                pass
        """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        assert result.ret == 0
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_dependent_testmodule_failures_accumulating(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            def test_1():
                pass
        """
        )
        local_remote.makepyfile(
            test_b="""
            import test_a
            def test_2():
                test_a.test_1()
                raise Exception()
        """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.assert_outcomes(1, 0, 1)

        tf = local_remote.makepyfile(
            test_b="""
            import test_a
            def test_2():
                pass
        """
        )
        tf.setmtime(1)
        result = local_remote.runpytest_inprocess("--testmon-dev-forceselect", "--lf")
        assert result.ret == 0
        result.assert_outcomes(1, 0, 0)

        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_dependent_testmodule_collect_ignore_error(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            def test_1():
                pass

            def a():
                pass
        """
        )
        local_remote.makepyfile(
            test_b="""
            import test_a
            def test_2():
                test_a.a()
                pass
                        """
        )
        local_remote.runpytest_inprocess("--testmon-dev")

        tf = local_remote.makepyfile(
            test_b="""
            import test_a
            def test_2():
                test_a.a()
                pass
                pass
        """
        )
        tf.setmtime(1)
        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_collection_not_abort(self, local_remote):
        local_remote.makepyfile(
            test_collection_not_abort="""
            def test_1():
                1

            def test_2():
                assert False
                """
        )

        local_remote.runpytest_inprocess("--testmon-dev")

        tf = local_remote.makepyfile(
            test_collection_not_abort="""
            def test_1():
                2

            def test_2():
                assert False
        """
        )
        tf.setmtime(1)

        result = local_remote.runpytest_inprocess("-v", "--testmon-dev")

        result.stdout.fnmatch_lines(
            [
                "*test_collection_not_abort.py::test_2 FAILED*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_failures_storage_retrieve(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            import pytest

            @pytest.fixture
            def error():
                raise Exception()

            def test_b(error):
                assert 1
        """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.assert_outcomes(0, 0, 0, 1)

        result = local_remote.runpytest_inprocess("--testmon-dev")
        result.assert_outcomes(0, 0, 0, 1)
        result.stdout.fnmatch_lines(
            [
                "*1 error*",
            ]
        )

    def test_syntax_error(self, testdir):
        testdir.makepyfile(
            test_a="""\
            def test_1():
                pass
        """
        )
        testdir.runpytest_inprocess("--testmon-dev")

        testdir.makepyfile(
            test_a="""\
            def test_1():
                1 = 2
        """
        )
        result = testdir.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(["*ERROR collecting test_a.py*"])

    def test_update_mtimes(self, testdir):
        testdir.makepyfile(
            test_a="""
            def test_1():
                pass
            def test_2():
                pass
        """
        )
        testdir.runpytest_inprocess("--testmon-dev")
        testdir.makepyfile(
            test_a="""
            def test_1():
                a=1
                pass
            def test_2():
                pass
        """
        )
        result = testdir.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*changed files: test_a.py*",
            ]
        )

        result = testdir.runpytest_inprocess("--testmon-dev-nocollect")
        result.stdout.fnmatch_lines(
            [
                "*changed files: 0*",
            ]
        )


class TestPytestCollectionPhase:
    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_sync_after_collectionerror(self, local_remote):
        local_remote.makepyfile(
            test_a="""
                def test_0():
                    pass

                def test_2():
                    pass
            """
        )
        local_remote.runpytest_inprocess(
            "--testmon-dev",
        )
        local_remote.makepyfile(
            test_a="""
                def test_0():
                    pass

                def test_2():
                    try: # This is wrong syntax and will cause collection error.
            """
        )
        local_remote.runpytest_inprocess(
            "--testmon-dev",
        )
        local_remote.makepyfile(
            test_a="""
                def test_0():
                    pass

                def test_2():
                    print(1)
            """
        )
        result = local_remote.runpytest_inprocess("--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*test_2 PASSED*",
            ]
        )


while_running_condition = Condition()


class TestmonCollect:
    @pytest.mark.xfail
    def test_change_while_running_no_data(self, testdir):
        def make_second_version(condition):
            with condition:
                condition.wait()
                t = testdir.makepyfile(test_a=test_template.replace("$r", "2 == 3"))
                t.setmtime(2640053809)

        test_template = """
                import tests.test_testmon

                with tests.test_testmon.while_running_condition:
                    tests.test_testmon.while_running_condition.notify()

                def test_1():
                    assert $r
            """

        testdir.makepyfile(test_a=test_template.replace("$r", "1 == 1"))
        thread = Thread(
            target=make_second_version, args=(while_running_condition,)
        )  # wait for the
        # test execution and change test_a.py to version 2
        thread.start()
        testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        thread.join()

        result = testdir.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*1 failed*",
            ]
        )

    def test_change_while_running_with_data(self, testdir):
        def make_third_version(condition):
            with condition:
                condition.wait()
                t = testdir.makepyfile(test_a=test_template.replace("$r", "2 == 3"))
                t.setmtime(2640053809)

        test_template = """
                    import tests.test_testmon

                    with tests.test_testmon.while_running_condition:
                        tests.test_testmon.while_running_condition.notify()

                    def test_1():
                        assert $r
                """

        # creating test v1
        testdir.makepyfile(test_a=test_template.replace("$r", "1 == 1"))

        # executing testmon to create data
        result = testdir.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

        # creating test v2
        file = testdir.makepyfile(test_a=test_template.replace("$r", "2 == 2"))
        file.setmtime(2640044809)

        # creating test v3 and waiting to replace test's code
        thread = Thread(target=make_third_version, args=(while_running_condition,))
        thread.start()

        result = testdir.runpytest_inprocess("--testmon-dev")

        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

        thread.join()

        # executing test v3
        result = testdir.runpytest_inprocess("--testmon-dev")
        result.stdout.fnmatch_lines(
            [
                "*1 failed*",
            ]
        )

    def test_failed_setup_phase(self, testdir):
        testdir.makepyfile(
            fixture="""
                import pytest

                @pytest.fixture
                def fixturetest():
                    raise Exception("from fixture")
        """,
            test_a="""
            from fixture import fixturetest
            def test_1(fixturetest):
                pass
        """,
        )
        testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        td = CoreTestmonData("")
        assert td.all_files == {"fixture.py", "test_a.py"}

    def test_remove_dependent_file_subdir_1(self, testdir):
        source_subdir_path = testdir.mkpydir("source")
        src_a = """
            def add(a, b):
                return a + b
            """

        source_file = write_source_code_to_a_file(source_subdir_path / "a.py", src_a)

        src_test_a = """
                from source.a import add
                def test_add():
                    assert add(1, 2) == 3
                """
        tests_subdir_path = testdir.mkpydir("testing")

        write_source_code_to_a_file(tests_subdir_path / "test_a.py", src_test_a)

        result = testdir.runpytest_inprocess("--testmon-dev")
        assert result.ret == 0

        source_file.remove()
        result = testdir.runpytest_inprocess("--testmon-dev", "--tb=long", "-v")

        result.stdout.fnmatch_lines(
            [
                "*ImportError*",
            ]
        )

    def test_remove_dependent_file_subdir_2(self, testdir):
        source_subdir_path = testdir.mkpydir("source")
        tests_subdir_path = testdir.mkpydir("testing")
        src = """
            def add(a, b):
                return a + b
            """
        sourcefile = write_source_code_to_a_file(source_subdir_path / "a.py", src)

        src_2 = """
                def test_add():
                    from source.a import add
                    assert add(1, 2) == 3
                """
        write_source_code_to_a_file(tests_subdir_path / "test_a.py", src_2)

        result = testdir.runpytest_inprocess("--testmon-dev")
        assert result.ret == 0

        sourcefile.remove()
        result = testdir.runpytest_inprocess("--testmon-dev", "--tb=long", "-v")
        result.stdout.fnmatch_lines(
            [
                "*test_a.py::test_add FAILED*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_remove_dependent_file(self, local_remote):
        local_remote.makepyfile(
            lib="""
                def oneminus(a):
                    return a - 1
        """,
            test_a="""
                from lib import oneminus
                def test_1():
                    oneminus(1)
        """,
        )
        local_remote.runpytest_inprocess(
            "--testmon-dev",
        )
        f = local_remote.makepyfile(
            test_a="""
            def test_1():
                pass
        """
        )
        f.setmtime(12345)
        local_remote.runpytest_inprocess(
            "--testmon-dev",
        )
        td = local_remote.td
        assert set(td.db.filenames(td.exec_id)) == {"test_a.py"}

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_pytest_k_deselect(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            def test_1():
                pass
            def test_2():
                pass
        """
        )
        local_remote.runpytest_inprocess("--testmon-dev", "-k test_1")
        time.sleep(0.1)
        local_remote.makepyfile(
            test_a="""
            def test_1():
                pass
            def test_2():
                print()
        """
        )
        result = local_remote.runpytest_inprocess("--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*test_2 PASSED*",
            ]
        )

    def test_pytest_argument_deselect(self, testdir):
        testdir.makepyfile(
            test_a="""
            def test_1():
                pass
            def test_2():
                pass
        """
        )

        testdir.runpytest_inprocess("--testmon-dev", "test_a.py::test_1")
        time.sleep(0.1)
        testdir.makepyfile(
            test_a="""
            def test_1():
                pass
            def test_2():
                print()
        """
        )
        result = testdir.runpytest_inprocess("--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*test_2 PASSED*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_pytest_specified_test_noselect(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            def test_1():
                pass
            def test_2():
                pass
        """
        )

        local_remote.runpytest_inprocess("--testmon-dev")
        result = local_remote.runpytest_inprocess(
            "--testmon-dev", "-v", "test_a.py::test_1"
        )
        result.stdout.fnmatch_lines(
            [
                (
                    "*: selection automatically deactivated "
                    "because you selected tests manually*"
                ),
                "*test_1 PASSED*",
            ]
        )

    @pytest.mark.parametrize("local_remote", tm_flavors(), indirect=True)
    def test_external_deselect_garbage(self, local_remote):
        local_remote.makepyfile(
            test_a="""
            def test_1():
                pass
            def test_2():
                pass
        """
        )
        local_remote.runpytest_inprocess("--testmon-dev")
        time.sleep(0.1)
        local_remote.makepyfile(
            test_a="""
            def test_1():
                print()
            def test_2():
                print(2)
        """
        )
        local_remote.runpytest_inprocess("--testmon-dev", "-v", "-k test_1")
        time.sleep(0.1)
        local_remote.makepyfile(
            test_a="""
            def test_1():
                print()
            def test_2():
                print()
        """
        )

        result = local_remote.runpytest_inprocess("--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*test_2 PASSED*",
            ]
        )

    def test_dogfooding_allowed(self, testdir):
        testdir.makepyfile(
            test_a="""
            pytest_plugins = "pytester",
            def test_nested_test(testdir):
                testdir.makepyfile(
                    test_nested='''
                    def test_1():
                        assert True
                '''
                )
                result = testdir.runpytest_inprocess("-v", "--testmon-dev")
                result.assert_outcomes(1, 0, 0)
        """
        )

        result = testdir.runpytest_inprocess("-v", "--testmon-dev")
        result.assert_outcomes(1, 0, 0)


class TestDoctest:
    def test_track_doctest_modules(self, testdir, monkeypatch):
        a = testdir.makepyfile(
            test_a='''\
                        def a():
                            return 1
                        class KLASS:
                            """
                            >>> a()
                            2
                            """
                    '''
        )

        def func():
            testdir.runpytest_inprocess("test_a.py", "--doctest-modules")

        deps = track_it(testdir, func)

    def test_doc_test(self, testdir):
        doctestfile = testdir.maketxtfile(
            test_doc="""
                >>> 1
                1
            """
        )
        result = testdir.runpytest_inprocess("--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )
        doctestfile.setmtime(1)
        result = testdir.runpytest_inprocess("--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*no tests ran*",
            ]
        )

    def test_doctest_modules_identical(self, testdir):
        doctestfile = testdir.makepyfile(
            test_doc='''
                def a():
                    return 1
                class Klass:
                    """
                    >>> a()
                    1
                    """
            '''
        )
        result = testdir.runpytest_inprocess("--doctest-modules", "--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )
        doctestfile.setmtime(1)
        result = testdir.runpytest_inprocess("--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*no tests ran*",
            ]
        )

    def test_doctest_modules_changed(self, testdir):
        doctestfile = testdir.makepyfile(
            test_doc='''
                def a():
                    return 1
                class Klass:
                    """
                    >>> a()
                    1
                    """
            '''
        )
        result = testdir.runpytest_inprocess("--doctest-modules", "--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )
        doctestfile = testdir.makepyfile(
            test_doc='''
                def a():
                    return 1
                class Klass:
                    """
                    >>> a() + 0
                    1
                    """
            '''
        )
        doctestfile.setmtime(1)
        result = testdir.runpytest_inprocess(
            "--testmon-dev",
            "--doctest-modules",
            "-v",
        )
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

    def test_doc_test_changed(self, testdir):
        testdir.maketxtfile(
            test_doc="""
                >>> 1
                1
            """
        )
        result = testdir.runpytest_inprocess("--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )
        doctestfile = testdir.maketxtfile(
            test_doc="""
                >>> 1 + 0
                1
            """
        )
        doctestfile.setmtime(1)
        result = testdir.runpytest_inprocess("--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )

    def test_doc_test_inderect_change(self, testdir):
        testdir.makepyfile(
            libdoctest="""\
                           def a():
                               return 1
                            """
        )
        testdir.maketxtfile(
            test_doc="""
                >>> import libdoctest
                >>> libdoctest.a()
                1
            """
        )
        result = testdir.runpytest_inprocess("--testmon-dev", "-v", syspathinsert=True)
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )
        changepyfile(
            testdir,
            libdoctest="""\
                          def a():
                              return 1 + 0
                          """,
        )

        result = testdir.runpytest_inprocess("--testmon-dev", "-v")
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )


class TestLineAlgEssentialProblems:
    def test_add_line_at_beginning(self, testdir):
        testdir.makepyfile(
            test_a="""
            def test_a():
                assert 1 + 2 == 3
        """
        )
        testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        testdir.makepyfile(
            test_a="""
            def test_a():
                1/0
                assert 1 + 2 == 3
        """
        )
        result = testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        result.stdout.fnmatch_lines(
            [
                "*1 failed*",
            ]
        )

    def test_add_line_at_end(self, testdir):
        testdir.makepyfile(
            test_a="""
                   def test_a():
                       assert 1 + 2 == 3
               """
        )
        testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        testdir.makepyfile(
            test_a="""
                   def test_a():
                       assert 1 + 2 == 3
                       1/0
                """
        )
        result = testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        result.stdout.fnmatch_lines(
            [
                "*1 failed*",
            ]
        )

    def test_remove_method_definition(self, testdir):
        testdir.makepyfile(
            test_a="""
                           def test_1():
                               assert 1 + 2 == 3

                           def test_2():
                               assert 2 + 2 == 4
                       """
        )
        testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        testdir.makepyfile(
            test_a="""
                           def test_1():
                               assert 1 + 2 == 3

                               assert 2 + 2 == 4
                        """
        )
        result = testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        result.stdout.fnmatch_lines(
            [
                "*1 passed*",
            ]
        )


class TestPrioritization:
    def test_module_level(self, testdir):
        testdir.makepyfile(
            test_a="""
                            import time
                            def test_a():
                                time.sleep(0.5)
                        """
        )
        testdir.makepyfile(
            test_b="""
                            import time
                            def test_b():
                                time.sleep(0.1)
                        """
        )

        testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        a = testdir.makepyfile(
            test_a="""
                            import time
                            def test_a():
                                a=1
                        """
        )
        b = testdir.makepyfile(
            test_b="""
                            import time
                            def test_b():
                                b=1
                        """
        )
        a.setmtime(1424880935)
        b.setmtime(1424880935)
        result = testdir.runpytest_inprocess("--testmon-dev-nocollect")
        result.stdout.fnmatch_lines(
            [
                "test_b.py*",
                "test_a.py*",
            ]
        )

    def test_class_level(self, testdir):
        testdir.makepyfile(
            test_m="""
                import time
                class TestA:
                    def test_a(self):
                        time.sleep(0.5)

                class TestB:
                    def test_b(self):
                        time.sleep(0.1)
            """
        )
        testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        m = testdir.makepyfile(
            test_m="""
                            import time
                            class TestA:
                                def test_a(self):
                                    a=1

                            class TestB:
                                def test_b(self):
                                    b=1
                        """
        )
        m.setmtime(1424880935)
        result = testdir.runpytest_inprocess("--testmon-dev-nocollect", "-v")
        result.stdout.fnmatch_lines(
            [
                "*TestB*",
                "*TestA*",
            ]
        )

    def test_node_level(self, testdir):
        testdir.makepyfile(
            test_m="""
                import time
                def test_a():
                    time.sleep(0.1)

                def test_b():
                    pass
            """
        )
        testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        m = testdir.makepyfile(
            test_m="""
                def test_a():
                    a=1

                def test_b():
                    b=1
            """
        )
        m.setmtime(1424880935)
        result = testdir.runpytest_inprocess("--testmon-dev-nocollect", "-v")
        result.stdout.fnmatch_lines(
            [
                "*test_b*",
                "*test_a*",
            ]
        )

    def test_noselect_sorts(self, testdir):
        testdir.makepyfile(
            test_m="""
                import time
                def test_a():
                    time.sleep(0.51)

                def test_b():
                    time.sleep(.34)

                def test_c():
                    time.sleep(.17)

                def test_d():
                    pass
            """
        )
        testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        m = testdir.makepyfile(
            test_m="""
                import time
                def test_a():
                    time.sleep(0.511)

                def test_b():
                    time.sleep(.341)

                def test_c():
                    time.sleep(.17)

                def test_d():
                    pass
            """
        )
        m.setmtime(1424880935)
        result = testdir.runpytest_inprocess("--testmon-dev-noselect", "-v")
        result.stdout.fnmatch_lines(
            [
                "*test_b*",
                "*test_a*",
                "*test_d*",
                "*test_c*",
            ]
        )

    def test_noselect_ignore_collect(self, testdir):
        testdir.makepyfile(
            test_m1="""
                import time
                def test_a():
                    time.sleep(0.09)
            """,
            test_m2="""
                def test_b():
                    pass
            """,
        )
        testdir.runpytest_inprocess(
            "--testmon-dev",
        )
        m = testdir.makepyfile(
            test_m1="""
                import time
                def test_a():
                    time.sleep(0.091)
            """,
        )
        m.setmtime(1424880935)
        result = testdir.runpytest_inprocess("--testmon-dev-noselect", "-v")
        result.stdout.fnmatch_lines(
            [
                "*test_a*",
                "*test_b*",
            ]
        )

    def test_report_failed_stable_last(self, testdir):
        testdir.makepyfile(
            test_m="""
                           def test_a():
                               assert False

                           def test_b():
                               b = 1
                       """
        )
        testdir.runpytest_inprocess(
            "--testmon-dev",
        )

        m = testdir.makepyfile(
            test_m="""
                           def test_a():
                               assert False

                           def test_b():
                               b = 2
                       """
        )
        m.setmtime(1424880935)
        result = testdir.runpytest_inprocess("--testmon-dev-nocollect", "-v")
        result.stdout.fnmatch_lines(["*test_a FAILED*"])

    def test_interrupted2(self, testdir):
        testdir.makepyfile(
            test_m="""
                import time
                def test_a():
                   time.sleep(0.01)

                def test_b():
                   time.sleep(0.10)

                def test_c():
                   time.sleep(0.2)
           """
        )
        testdir.runpytest_inprocess(
            "--testmon-dev",
        )

        testdir.makepyfile(
            test_m="""
                import time
                def test_a():
                   time.sleep(0.011)

                def test_b():
                   raise KeyboardInterrupt

                def test_c():
                   time.sleep(0.201)
           """
        )

        testdir.runpytest_subprocess("--testmon-dev", "-v", "--full-trace")

        testdir.makepyfile(
            test_m="""
                import time
                def test_a():
                   time.sleep(0.011)

                def test_b():
                   time.sleep(0.102)

                def test_c():
                   time.sleep(0.202)
           """
        )
        result = testdir.runpytest_inprocess("--testmon-dev", "-v")

        result.stdout.no_fnmatch_line("*test_a PASSED*")

        result.stdout.fnmatch_lines(
            [
                "*test_b PASSED*",
                "*test_c PASSED*",
            ]
        )


# #ifdef PYTEST_COV
class TestPlusCov:
    @pytest.mark.skipif(
        "cov" not in os.environ.get("TOX_ENV_NAME", "cov"),
        reason="requires pytest-cov in TOX",
    )
    def test_simple(self, testdir):
        testdir.makepyfile(
            test_a="""\
        import os
        import pytest_cov
        def test_1():
            print(1928)
        """
        )
        result = testdir.runpytest_subprocess(
            "-v", "--testmon-dev", "--cov=.", "-s", "--cov-report", "term-missing"
        )
        td = CoreTestmonData("")
        result.stdout.fnmatch_lines(["*test_a.py       4      0   100%*"])
        checksums = blob_to_checksums(
            td.db.con.execute("select method_checksums from file_fp").fetchone()[
                "method_checksums"
            ]
        )
        assert create_fingerprint_source("print(1928)", {1})[0] in checksums

    @pytest.mark.skipif(
        "cov" not in os.environ.get("TOX_ENV_NAME", "cov"),
        reason="requires pytest-cov in TOX",
    )
    def test_omit_hit(self, testdir):
        rc = testdir.maketxtfile(
            rc="""
                [run]
                omit = test_a.py
                """
        )
        testdir.makepyfile(
            test_a="""
               import os
               import pytest_cov
               def test_1():
                   print(1928)
                   """,
            test_b="""
               pass
            """,
        )

        result = testdir.runpytest_subprocess(
            "-v", "--cov=.", f"--cov-config={rc}", "-s", "--testmon-dev"
        )
        result.stdout.no_fnmatch_line("test_a.py **")
        result.stdout.fnmatch_lines(["TOTAL           1      0   100%"])
        td = CoreTestmonData("")
        checksums = blob_to_checksums(
            td.db.con.execute("select method_checksums from file_fp").fetchone()[
                "method_checksums"
            ]
        )
        assert create_fingerprint_source("print(1928)", {1})[0] in checksums

    @pytest.mark.skipif(
        "cov" not in os.environ.get("TOX_ENV_NAME", "cov"),
        reason="requires pytest-cov in TOX",
    )
    def test_src(self, testdir):
        testdir.mkpydir("src")

        testdir.makepyfile(
            test_b="""
                    import os
                    import pytest_cov
                    def test_1():
                        print(1928)
        """
        )

        result = testdir.runpytest_subprocess(
            "-v",
            "--testmon-dev",
            "--cov=src",
            "-s",
        )
        result.stdout.fnmatch_lines(["src/__init__.py       0      0   100%*"])
        result.stdout.fnmatch_lines(["TOTAL                 0      0   100%*"])

        td = CoreTestmonData("")
        checksums = blob_to_checksums(
            td.db.con.execute("select method_checksums from file_fp").fetchone()[
                "method_checksums"
            ]
        )
        assert create_fingerprint_source("print(1928)", {1})[0] in checksums


# #endif


class TestXdist(object):
    @pytest.mark.skipif(
        "xdist" not in os.environ.get("TOX_ENV_NAME", "xdist"),
        reason="requires pytest-xdist in TOX",
    )
    def test_xdist_4(self, testdir):
        testdir.makepyfile(
            test_a="""
            import pytest
            def test_0():
                1

            @pytest.mark.parametrize("a", [
                                    ("test0", ),
                                    ("test1", ),
                                    ("test2", ),
                                    ("test3", )
            ])
            def test_1(a):
                print(a)
            """
        )

        testdir.runpytest_inprocess(
            "test_a.py::test_0", "--testmon-dev", "-v"
        )  # xdist is not supported on the first run
        time.sleep(0.1)
        result = testdir.runpytest_inprocess("test_a.py", "--testmon-dev", "-n 4", "-v")
        # #ifdef XDIST
        result.stdout.fnmatch_lines(["testmon-dev:*", "*PASSED test_a.py::test_1[a0*"])
        return
        # #endif
        result.stdout.fnmatch_lines(
            [
                "*deactivated, execution with xdist is not supported*",
            ]
        )

    @pytest.mark.skipif(
        "xdist" not in os.environ.get("TOX_ENV_NAME", "xdist"),
        reason="requires pytest-xdist in TOX",
    )
    def test_parallelistm_status_single(self, testdir):
        testdir.makeconftest(
            """
            from testmon_dev.pytest_testmon import parallelism_status
            def pytest_configure(config):
                assert parallelism_status(config) == 'single'
        """
        )
        testdir.makepyfile(
            test_a="""
            from testmon_dev.pytest_testmon import parallelism_status
            def test_1(request):
                assert parallelism_status(request.config) == 'single'
            """
        )

        result = testdir.runpytest_inprocess("--testmon-dev")
        assert result.ret == 0

    @pytest.mark.skipif(
        "xdist" not in os.environ.get("TOX_ENV_NAME", "xdist"),
        reason="requires pytest-xdist in TOX",
    )
    def test_parallelistm_status_worker(self, testdir):
        testdir.makepyfile(
            test_a="""
            from testmon_dev.pytest_testmon import parallelism_status
            def test_1(request):
                assert parallelism_status(request.config) == "worker"
            """
        )
        result = testdir.runpytest_inprocess("--testmon-dev", "-n1")
        assert result.ret == 0


class TestForcedFlag(object):
    def test_fresh_run(self, testdir):
        testdir.makepyfile(
            test_a="""
            def test_1():
                assert 1==1

            def test_2():
                assert 1==1
            """
        )
        testdir.runpytest_inprocess("--testmon-dev")
        testmon_data = CoreTestmonData("")
        assert (
            2
            == testmon_data.db.con.execute(
                "SELECT count(*) FROM test_execution WHERE forced IS NOT NULL"
            ).fetchone()[0]
        )

    def test_one_changed(self, testdir):
        testdir.makepyfile(
            test_a="""
            def test_1():
                assert 1==1

            def test_2():
                assert 1==1
            """
        )
        testdir.runpytest_inprocess("--testmon-dev")
        testdir.makepyfile(
            test_a="""
            def test_1():
                assert 1==1

            def test_2():
                assert 2==2
            """
        )
        testdir.runpytest_inprocess("--testmon-dev")
        testmon_data = CoreTestmonData("")
        assert (
            testmon_data.db.con.execute(
                "SELECT count(*) FROM test_execution WHERE forced IS NULL"
            ).fetchone()[0]
            == 1
        )
        assert (
            testmon_data.db.con.execute(
                "SELECT count(*) FROM test_execution WHERE forced == 0"
            ).fetchone()[0]
            == 1
        )
        assert (
            testmon_data.db.con.execute(
                "SELECT count(*) FROM test_execution WHERE forced == 1"
            ).fetchone()[0]
            == 0
        )


class TestStats:
    def test_savings_tests(self, testdir):
        testdir.makepyfile(
            test_a="""
                    def test_1():
                        pass
                   """
        )
        testdir.runpytest_subprocess("--testmon-dev")
        td = CoreTestmonData("")
        assert td.db.fetch_attribute(attribute="tests_all") == 1
        assert td.db.fetch_attribute(attribute="tests_saved") == 0
        testdir.runpytest_subprocess("--testmon-dev")
        assert td.db.fetch_attribute(attribute="tests_saved") == 1
        assert td.db.fetch_attribute(attribute="tests_all") == 2

    @pytest.mark.skipif(sys.platform == "win32", reason="Windows platform")
    def test_savings_time(self, testdir):
        testdir.makepyfile(
            test_a="""
                    def test_1():
                        pass
                   """
        )
        testdir.runpytest_subprocess("--testmon-dev")
        td = CoreTestmonData("")
        assert td.db.fetch_attribute(attribute="time_saved") == 0
        assert td.db.fetch_attribute(attribute="time_all") > 0
        testdir.runpytest_subprocess("--testmon-dev")
        assert td.db.fetch_attribute(attribute="time_saved") > 0
