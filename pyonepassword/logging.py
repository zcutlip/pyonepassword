import logging

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING


def console_logger(name: str, level: int):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    logger.addHandler(ch)

    return logger


def console_debug_logger(name: str):
    logger = console_logger(name, DEBUG)
    return logger
