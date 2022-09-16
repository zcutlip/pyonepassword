import logging

DEBUG = logging.DEBUG
INFO = logging.INFO


def console_logger(name: str, level: int):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    logger.addHandler(ch)

    return logger
