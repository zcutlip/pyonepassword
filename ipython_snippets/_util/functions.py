import pathlib

from pyonepassword import OP
from pyonepassword.logging import console_debug_logger


def snippet_dir():
    main_file = pathlib.Path(__file__)
    main_dir = main_file.parent.parent
    return main_dir


def scratch_dir():
    main_dir = snippet_dir()
    scratch = pathlib.Path(main_dir, "scratch")
    scratch.mkdir(exist_ok=True)
    return scratch


def get_op(logger_name):
    logger = console_debug_logger(logger_name)
    op = OP(logger=logger)
    return op
