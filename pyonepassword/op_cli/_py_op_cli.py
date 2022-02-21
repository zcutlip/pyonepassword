import logging
import subprocess

from os import environ as env

from ._op_argv_base import _OPArgvBase
from ._op_argv_v1 import _OPArgv as _OPArgvV1
from .._op_cli_config import OPCLIConfig
from ..op_cli_version import OPCLIVersion

from ..py_op_exceptions import (
    OPSigninException,
    OPNotSignedInException,
    OPNotFoundException,
    OPCmdFailedException,
)
from .._py_op_deprecation import deprecated

"""
Module to hold stuff that interacts directly with 'op' or its config

TODO: Move other code that closely touches 'op' here
"""


class _OPCLIExecute:
    NOT_SIGNED_IN_TEXT = "not currently signed in"

    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    logger = logging.getLogger()
    """
    Class for logging into and querying a 1Password account via the 'op' cli command.
    """
    OP_PATH = 'op'  # let subprocess find 'op' in the system path

    def __init__(self,
                 account_shorthand=None,
                 signin_address=None,
                 email_address=None,
                 secret_key=None,
                 password=None,
                 logger=None,
                 op_path='op',
                 use_existing_session=False,
                 password_prompt=True):
        """
        Create an OP object. The 1Password sign-in happens during object instantiation.
        If 'password' is not provided, the 'op' command will prompt on the console for a password.

        If all components of a 1Password account are provided, an initial sign-in is performed,
        otherwise, a normal sign-in is performed. See `op --help` for further explanation.

        Arguments:
            - 'account_shorthand': The shorthand name for the account on this device.
                                   You may choose this during initial signin, otherwise
                                   1Password converts it from your account address.
                                   See 'op signin --help' for more information.
            - 'signin_address': Fully qualified address of the 1Password account.
                                E.g., 'my-account.1password.com'
            - 'email_address': Email of the address for the user of the account
            - 'secret_key': Secret key for the account
            - 'password': The user's master password
            - 'logger': A logging object. If not provided a basic logger is created and used.
            - 'op_path': optional path to the `op` command, if it's not at the default location

        Raises:
            - OPSigninException if 1Password sign-in fails for any reason.
            - OPNotFoundException if the 1Password command can't be found.
        """
        if logger:
            self.logger = logger
        self._cli_version: OPCLIVersion = self._get_cli_version(op_path)
        if account_shorthand is None:
            config = OPCLIConfig()
            try:
                account_shorthand = config['latest_signin']
                self.logger.debug(
                    "Using account shorthand found in op config: {}".format(account_shorthand))
            except KeyError:
                account_shorthand = None

        if account_shorthand is None:
            raise OPNotSignedInException(
                "Account shorthand not provided and not found in 'op' config")

        sess_var_name = 'OP_SESSION_{}'.format(account_shorthand)

        self._token = None

        self.account_shorthand = account_shorthand
        self.op_path = op_path

        initial_signin_args = [account_shorthand,
                               signin_address,
                               email_address,
                               secret_key,
                               password]
        initial_signin = (None not in initial_signin_args)

        if use_existing_session:
            self._token = self._verify_signin(sess_var_name)

        if not self._token:
            if not password and not password_prompt:
                raise OPNotSignedInException(
                    "No existing session and no password provided.")
            if initial_signin:
                self._token = self._do_initial_signin(*initial_signin_args)
                # export OP_SESSION_<signin_address>
            else:
                self._token = self._do_normal_signin(
                    account_shorthand, password)

        # TODO: return already-decoded token from sign-in
        self._sess_var = sess_var_name
        env[sess_var_name] = self.token

    @property
    def token(self) -> str:
        return self._token

    @property
    def session_var(self) -> str:
        return self._sess_var

    def _get_cli_version(self, op_path):
        argv = _OPArgvBase.cli_version_argv(op_path)
        output = self._run(argv, capture_stdout=True, decode="utf-8")
        output = output.rstrip()
        cli_version = OPCLIVersion(output)
        return cli_version

    def _verify_signin(self, sess_var_name):
        # Need to get existing token if we're already signed in
        token = env.get(sess_var_name)

        if token:
            # if there's no token, no need to sign in
            argv = _OPArgvV1.get_verify_signin_argv(self.op_path)
            try:
                self._run(argv, capture_stdout=True)
            except OPCmdFailedException as opfe:
                # scrape error message about not being signed in
                # invalidate token if we're not signed in
                if self.NOT_SIGNED_IN_TEXT in opfe.err_output:
                    token = None
                else:
                    # there was a different error so raise the exception
                    raise opfe

        return token

    def _do_normal_signin(self, account_shorthand, password):
        self.logger.info("Doing normal (non-initial) 1Password sign-in")
        signin_argv = _OPArgvV1.normal_signin_argv(
            self.op_path, account_shorthand=account_shorthand)

        token = self._run_signin(signin_argv, password=password).rstrip()
        return token.decode()

    @deprecated("Initial sign-in soon to be deprecated due to incompatibility with multi-factor authentication")
    def _do_initial_signin(self, account_shorthand, signin_address, email_address, secret_key, password):
        self.logger.info(
            "Performing initial 1Password sign-in to {} as {}".format(signin_address, email_address))
        signin_argv = [self.op_path, "signin", signin_address,
                       email_address, secret_key, "--raw"]
        if account_shorthand:
            signin_argv.extend(["--shorthand", account_shorthand])

        token = self._run_signin(signin_argv, password=password).rstrip()

        return token.decode()

    def _run_signin(self, argv, password=None):
        try:
            output = self._run(argv, capture_stdout=True,
                               input_string=password)
        except OPCmdFailedException as opfe:
            raise OPSigninException.from_opexception(opfe) from opfe

        return output

    @classmethod
    def _run_raw(cls, argv, input_string=None, capture_stdout=False, ignore_error=False):
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
                raise OPCmdFailedException(stderr_output, returncode) from err

        return (stdout, stderr, returncode)

    @classmethod
    def _run(cls, argv, capture_stdout=False, input_string=None, decode=None):
        output = None
        try:
            output, _, _ = cls._run_raw(
                argv, input_string=input_string, capture_stdout=capture_stdout)
            if decode:
                output = output.decode(decode)
        except FileNotFoundError as err:
            cls.logger.error(
                "1Password 'op' command not found at: {}".format(argv[0]))
            cls.logger.error(
                "See https://support.1password.com/command-line-getting-started/ for more information,")
            cls.logger.error(
                "or install from Homebrew with: 'brew install 1password-cli")
            raise OPNotFoundException(argv[0], err.errno) from err

        return output
