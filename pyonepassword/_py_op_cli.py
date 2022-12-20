import logging
import subprocess
from os import environ

from .py_op_exceptions import OPCmdFailedException, OPNotFoundException

# Mainly for use in automated testing
LOG_OP_ERR_ENV_NAME = "LOG_OP_ERR"

"""
Module to hold stuff that interacts directly with 'op' or its config

TODO: Move other code that closely touches 'op' here
"""


class _OPCLIExecute:
    logger = logging.getLogger("_OPCLIExecute")
    logger.setLevel(logging.INFO)

    def __new__(cls, *args, logger=None, **kwargs):
        if logger:
            cls.set_logger(logger)
        return super().__new__(cls)
    """
    Class for logging into and querying a 1Password account via the 'op' cli command.
    """

    @classmethod
    def _run_raw(cls, argv, input_string=None, capture_stdout=False, ignore_error=False, env=environ):
        stdout = subprocess.PIPE if capture_stdout else None
        if input_string:
            if isinstance(input_string, str):
                input_string = input_string.encode("utf-8")

        _ran = subprocess.run(
            argv, input=input_string, stderr=subprocess.PIPE, stdout=stdout, env=env)

        stdout = _ran.stdout
        stderr = _ran.stderr
        returncode = _ran.returncode

        if not ignore_error:
            try:
                _ran.check_returncode()
            except subprocess.CalledProcessError as err:
                stderr_output = stderr.decode("utf-8").rstrip()
                if environ.get(LOG_OP_ERR_ENV_NAME) == "1":
                    cls.logger.error(stderr_output)
                raise OPCmdFailedException(stderr_output, returncode) from err

        return (stdout, stderr, returncode)

    @classmethod
    def _run(cls, argv, capture_stdout=False, input_string=None, decode=None, env=environ):
        cls.logger.debug(f"Running: {argv.cmd_str()}")
        output = None
        try:
            output, _, _ = cls._run_raw(
                argv, input_string=input_string, capture_stdout=capture_stdout, env=env)
            if decode and output is not None:
                output = output.decode(decode)
        except FileNotFoundError as err:
            cls.logger.error(
                "1Password 'op' command not found at: {}".format(argv[0]))
            cls.logger.error(
                "See https://developer.1password.com/docs/cli for more information")
            raise OPNotFoundException(argv[0], err.errno) from err

        return output

    @classmethod
    def set_logger(cls, logger: logging.Logger):
        cls.logger = logger

    @classmethod
    def set_log_level(cls, log_level: int):  # pragma: no coverage
        cls.logger.setLevel(log_level)
