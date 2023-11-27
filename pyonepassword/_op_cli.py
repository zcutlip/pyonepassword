import logging
import subprocess
from os import environ

from .py_op_exceptions import (
    OPCLIPanicException,
    OPCmdFailedException,
    OPNotFoundException,
    OPRevokedSvcAcctTokenException
)

# Mainly for use in automated testing
LOG_OP_ERR_ENV_NAME = "LOG_OP_ERR"

"""
Module to hold stuff that interacts directly with 'op' or its config

TODO: Move other code that closely touches 'op' here
"""


class _OPCLIExecute:
    # we need to detect if a command failure was actually a mock-op failure
    MOCK_OP_ERR_EXIT = 255
    MOCK_OP_RESP_ERR_MSG = "Error looking up response"
    GO_RUNTIME_PANIC_MSG = "panic: runtime error:"
    SVC_ACCT_REVOKED_MSG = "The Service Account used in this integration has been deleted"
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
    def _should_log_op_errors(cls) -> bool:
        should_log = False
        if environ.get(LOG_OP_ERR_ENV_NAME) == "1":
            should_log = True
        return should_log

    @classmethod
    def _run_raw(cls, argv, input=None, capture_stdout=False, ignore_error=False, env=environ):
        stdout = subprocess.PIPE if capture_stdout else None
        if input:
            if isinstance(input, str):
                input = input.encode("utf-8")

        _ran = subprocess.run(
            argv, input=input, stderr=subprocess.PIPE, stdout=stdout, env=env)

        stdout = _ran.stdout
        stderr = _ran.stderr
        returncode = _ran.returncode

        if not ignore_error:
            try:
                _ran.check_returncode()
            except subprocess.CalledProcessError as err:
                stderr_output = stderr.decode("utf-8").rstrip()
                if cls._should_log_op_errors():
                    cls.logger.error(f"'op' command error: {stderr_output}")
                # HACK:
                # mock-op returns -1 (i.e., 255) if it can't find a response
                # but op (currently) only ever returns 1 on error
                #
                # we need to check if this was a mock-op failure so that during
                # testing we can distinguish between a simulated 'op' command failure
                # and mock-op failing because we haven't provided an appropriate response
                # definition
                if (returncode >= cls.MOCK_OP_ERR_EXIT and
                        cls.MOCK_OP_RESP_ERR_MSG in stderr_output):  # pragma: no coverage
                    raise err
                elif cls.GO_RUNTIME_PANIC_MSG in stderr_output:
                    # If we made 'op' crash, raise a special exception
                    raise OPCLIPanicException(stderr_output, returncode, argv)
                elif cls.SVC_ACCT_REVOKED_MSG in stderr_output:
                    # do this unconditionally without checking if we're authed as
                    # a service account
                    # in case caller is accidentally running with OP_SERVICE_ACCOUNT_TOKEN
                    raise OPRevokedSvcAcctTokenException(
                        stderr_output, returncode)

                raise OPCmdFailedException(stderr_output, returncode) from err

        return (stdout, stderr, returncode)

    @classmethod
    def _run(cls, argv, capture_stdout=False, input=None, decode=None, env=environ):
        cls.logger.debug(f"Running: {argv.cmd_str()}")
        output = None
        try:
            output, _, _ = cls._run_raw(
                argv, input=input, capture_stdout=capture_stdout, env=env)
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
