#  -- coding:utf8 --
from pathlib import Path
from subprocess import run

import pytest

from testmon_dev.process_code import (
    Module,
    read_source_sha,
    match_fingerprint_source,
    create_fingerprint,
    create_fingerprint_source,
    get_source_sha,
)
from testmon_dev.testmon_core import SourceTree

try:
    from StringIO import StringIO as MemFile
except ImportError:
    from io import BytesIO as MemFile  # noqa: F401

from collections import namedtuple

pytest_plugins = ("pytester",)


class TestCreateAndMatchFingerprintRoundtrip:
    def test_minimal_module(self):
        fingerprint = create_fingerprint_source(
            """\
            print("a") # <
            """,
            {1},  # covered line numbers, also marked in the source.
        )
        assert (
            # this is used for deselection (before execution)
            # if fingerprint doesn't match test must be re-executed
            # otherwise next source file is checked against it's
            # fingerprint
            match_fingerprint_source(
                """\
                                                print("changed")
                                                """,
                fingerprint,
            )
            is False
        )

    def test_nonexecuted(self):
        fingerprint = create_fingerprint_source(
            """\
            print("a") # !
            """,
            {},  # module not executed at all
        )
        assert match_fingerprint_source(
            """\
            print("anything_should_match")
            """,
            fingerprint,
        )

    def test_module_level_change(self):
        fingerprint = create_fingerprint_source(
            """\
            print("a")    # <
            def test_1(): # <
                print(1)  # <
            """,
            {1, 2, 3},  # covered line numbers, also marked in the source.
        )
        assert (
            match_fingerprint_source(
                """\
                                                    print("changed")
                                                    def test_1():
                                                        print(1)
                                                    """,
                fingerprint,
            )
            is False
        )

    def test_method_change_unexecuted1(self):
        fingerprint = create_fingerprint_source(
            """\
            def test_1(): # <
                print(1)  # !
            def test_2(): # <
                print(2)  # <
            """,
            {1, 3, 4},  # covered line numbers, also marked in the source.
        )
        assert match_fingerprint_source(
            """\
            def test_1():
                whatever
            def test_2():
                print(2)
            """,
            fingerprint,
        )

    def test_method_change_unexecuted2(self):
        fingerprint = create_fingerprint_source(
            """\
            def test_1(): # <
                print(1)  # <
            def test_2(): # <
                print(2)  # !
            """,
            {1, 2, 3},  # covered line numbers, also marked in the source
        )
        assert match_fingerprint_source(
            """\
            def test_1():
                print(1)
            def test_2():
                whatever
            """,
            fingerprint,
        )

    def test_method_name_executed(self):
        fingerprint = create_fingerprint_source(
            """\
            def test_1(): # <
                print(1)  # <
            def test_2(): # <
                print(2)  # !
            """,
            {1, 2, 3},  # covered line numbers, also marked in the source
        )
        assert (
            match_fingerprint_source(
                """\
                                                    def test_changed():
                                                        print(1)
                                                    def test_2():
                                                        print(2)
                                                    """,
                fingerprint,
            )
            is False
        )

    def test_method_body_executed(self):
        fingerprint = create_fingerprint_source(
            """\
            def test_1(): # <
                print(1)  # <
            def test_2(): # <
                print(2)  # !
            """,
            {1, 2, 3},  # covered line numbers, also marked in the source
        )
        assert (
            match_fingerprint_source(
                """\
                                                    def test_1():
                                                        print("changed")
                                                    def test_2():
                                                        print(2)
                                                    """,
                fingerprint,
            )
            is False
        )

    def test_module_level_change2(self):
        fingerprint = create_fingerprint_source(
            """\
            def test_1(): # <
                print(1)  # !
            def test_2(): # <
                print(2)  # !
            """,
            {1, 3},  # covered line numbers, also marked in the source
        )
        assert match_fingerprint_source(
            """\
                def test_1():
                    print("changed")
                def test_2():
                    print("changed")
                """,
            fingerprint,
        )

    def test_method_name_unexecuted(self):
        # TODO introduce a different level of "change" because
        # a change in definition of method which hasn't been executed
        # is much less relevant then other changes. match_fingerprint should
        # return a ratio of match not just True/False
        fingerprint = create_fingerprint_source(
            """\
            def test_1(): # <
                print(1)  # <
            def test_2(): # <
                print(2)  # !
            """,
            {1, 2, 3},
        )
        assert (
            match_fingerprint_source(
                """\
                                                            def test_1():
                                                                print(1)
                                                            def test_changed():
                                                                print(2)
                                                    """,
                fingerprint,
            )
            is False
        )

    def test_doctest_same(self):
        fingerprint = create_fingerprint_source(
            """\
                >>> 1
                1
            """,
            {1},
            ext="txt",
        )
        assert match_fingerprint_source(
            """\
                >>> 1
                1
            """,
            fingerprint,
            ext="txt",
        )

    def test_doctest_different(self):
        fingerprint = create_fingerprint_source(
            """\
                >>> 1
                1
            """,
            {1},
            ext="txt",
        )
        assert not match_fingerprint_source(
            """\
                >>> 2
                2
            """,
            fingerprint,
            ext="txt",
        )


SAMPLESDIR = Path(__file__).parent / "samples"


class TestReadSrc:
    def test_read_file_with_checksum(self):
        assert "š" in read_source_sha(SAMPLESDIR / "print1250r.py")[0]

    def test_read_file_with_checksum_1250(self):
        _, checksum = read_source_sha(SAMPLESDIR / "print1250r.py")
        assert checksum == "e352deab2c4ee837f17e62ce1eadfeb898e76747"

    def test_read_empty_file_with_checksum(self):
        assert read_source_sha(SAMPLESDIR / "empty.py") == (
            "",
            "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
        )

    def test_read_nonexistent_file_with_checksum(self):
        assert read_source_sha(SAMPLESDIR / "notexist.py") == (
            None,
            None,
        )

    def test_read_file_with_checksum_no_newline_eof(self):
        _, checksum = read_source_sha(SAMPLESDIR / "no_newline_eof.py")
        assert checksum == "2ec482d52166df7d06bbb35c9f609520b370e498"

    def test_read_file_with_CR_NL(self):
        _, checksum = read_source_sha(SAMPLESDIR / "slash_r_n_file.py")
        assert checksum == "fdc00c4cb4c9620aa04f768706aab7fc29f68883"

    @pytest.mark.parametrize("ext", ["py", "p y"])
    def test_sha_git_file(self, testdir, ext):
        testdir.makefile(
            ext=ext,
            file="""
            pass

        """,
        )
        run(["git", "init"])
        run(["git", "add", f"file.{ext}"])

        source, checksum = get_source_sha(testdir.tmpdir.strpath, f"file.{ext}")
        assert checksum == "fc80254b619d488138a43632b617124a3d324702"
        assert source is None

    def test_sha_git_file_commit(self, testdir):
        testdir.makepyfile(
            filename="""
            pass

        """
        )
        run(["git", "init"])
        run(["git", "add", "filename.py"])
        run(["git", "commit", "-m", "Reasonable commit message"])
        source, checksum = get_source_sha(testdir.tmpdir.strpath, "filename.py")
        assert checksum == "fc80254b619d488138a43632b617124a3d324702"
        assert source is None

    def test_sha_git_change(self, testdir):
        testdir.makepyfile(filename=" ")
        run(["git", "init"])
        run(["git", "add", "filename.py"])
        testdir.makepyfile(
            filename="""
            pass

        """
        )

        source, checksum = get_source_sha(testdir.tmpdir.strpath, "filename.py")
        assert checksum == "fc80254b619d488138a43632b617124a3d324702"
        assert source is not None

    def test_sha_non_git_file(self):
        # This file will not be recognized as git file because of different path
        # sha will be calculated manually
        source, checksum = get_source_sha(str(SAMPLESDIR), "print1250r.py")
        assert checksum == "e352deab2c4ee837f17e62ce1eadfeb898e76747"
        assert source is not None


class CodeSample:
    def __init__(self, source_code, expected_coverage=None, possible_lines=None):
        self.source_code = source_code
        self.expected_coverage = expected_coverage or {}
        self.possible_lines = possible_lines or []


code_samples = {
    1: CodeSample(
        """\
        def add(a, b):
            return a + b

        assert add(1, 2) == 3
            """,
        [1, 2, 4],
    ),
    2: CodeSample(
        """\
        def add(a, b):
            return a + b

        def subtract(a, b):
            return a - b

        assert add(1, 2) == 3
            """,
        [1, 2, 4, 7],
    ),
    "3": CodeSample(
        """\
        class A(object):
            def add(self, a, b):
                return a + b
        """,
        [1, 2],
    ),
    "3b": CodeSample(
        """\
        class A(object):
            def add(self, a, b):
                return a - b
        """,
        [1, 2],
    ),
    "classes": CodeSample(
        """\
        class A(object):
            def add(self, a, b):
                return a + b
            def subtract(self, a, b):
                return a - b
        """,
        [1, 2, 4],
    ),
    "classes_b": CodeSample(
        """\
        class A(object):
            def add(self, a, b):
                return a + b
            def subtract(self, a, b):
                return a - b - 1
        """,
        [1, 2, 4],
    ),
    "classes_c": CodeSample(
        """\
        class A(object):
            def add1(self, a, b):
                return a + b
            def subtract(self, a, b):
                return a - b
        """,
        [1, 2, 4],
    ),
}


class TestModule:
    def test_read_source(self, testdir):
        testdir.makepyfile(
            a="""
            pass

        """
        )
        run(["git", "init"])
        run(["git", "add", "a.py"])
        run(["git", "commit", "-m", "Reasonable commit message"])
        module = SourceTree("").get_file("a.py")
        assert "pass" in module.source_code
