import logging

# #if TYPES

from typing import TypedDict, List, Dict


class FileFp(TypedDict):
    filename: str
    method_checksums: List[int] = None
    mtime: float = None  # optimization helper, not really a part of the data structure fundamentally
    checksum: int = None  # optimization helper, not really a part of the data structure fundamentally
    fingerprint_id: int = None  # optimization helper,


TestName = str

TestFileFps = Dict[TestName, List[FileFp]]

Duration = float
Failed = bool


class DepsNOutcomes(TypedDict):
    deps: List[FileFp]
    failed: Failed
    duration: Duration
    forced: bool = None


TestExecutions = Dict[TestName, DepsNOutcomes]


# #endif
def dummy():
    pass


def get_logger(name):
    logging.basicConfig(format="%(levelname)s: %(message)s.", level=logging.WARNING)
    return logging.getLogger(name)
