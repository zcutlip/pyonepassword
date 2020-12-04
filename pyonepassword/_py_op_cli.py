import os
import pathlib
import json
import logging
from json.decoder import JSONDecodeError
import subprocess
from os import environ as env

from .py_op_exceptions import (
    OPConfigNotFoundException,
    OPSigninException,
    OPNotFoundException,
    OPCmdFailedException

)
from ._py_op_deprecation import deprecated

"""
Module to hold stuff that interacts directly with 'op' or its config

TODO: Move other code that closely touches 'op' here
"""


class OPCLIConfig(dict):
    OP_CONFIG_RELPATH = os.path.join(".op", "config")

    def __init__(self, configpath=None):
        super().__init__()
        if configpath is None:
            configpath = self._get_config_path()

        if configpath is None:
            raise OPConfigNotFoundException("No op configuration found")

        try:
            config_json = open(configpath, "r").read()
        except FileNotFoundError as e:
            raise OPConfigNotFoundException(
                "op config not found at path: {}".format(configpath)) from e
        except PermissionError as e:
            raise OPConfigNotFoundException(
                "Permission denied accessing op config at path: {}".format(configpath)) from e

        try:
            config = json.loads(config_json)
            self.update(config)
        except JSONDecodeError as e:
            raise OPConfigNotFoundException(
                "Unable to json decode config at path: {}".format(configpath)) from e

    def _get_config_path(self):
        try:
            xdg_path = os.environ['XDG_CONFIG_HOME']
            configpath = os.path.join(xdg_path, self.OP_CONFIG_RELPATH)
        except KeyError:
            configpath = None

        if configpath is None:
            configpath = os.path.join(
                pathlib.Path.home(), self.OP_CONFIG_RELPATH)

        return configpath


class _OPCLIExecute:
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    logger = logging.getLogger()
    """
    Class for logging into and querying a 1Password account via the 'op' cli command.
    """
    OP_PATH = 'op'  # let subprocess find 'op' in the system path

    def __init__(self, account_shorthand=None, signin_address=None, email_address=None,
                 secret_key=None, password=None, logger=None, op_path='op'):
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

        if account_shorthand is None:
            config = OPCLIConfig()
            try:
                account_shorthand = config['latest_signin']
                self.logger.debug(
                    "Using account shorthand found in op config: {}".format(account_shorthand))
            except KeyError:
                account_shorthand = None

        if account_shorthand is None:
            raise OPSigninException(
                "Account shorthand not provided and not found in 'op' config")

        self.account_shorthand = account_shorthand
        self.op_path = op_path

        initial_signin_args = [account_shorthand,
                               signin_address,
                               email_address,
                               secret_key,
                               password]
        initial_signin = (None not in initial_signin_args)

        if initial_signin:
            self.token = self._do_initial_signin(*initial_signin_args)
            # export OP_SESSION_<signin_address>
        else:
            self.token = self._do_normal_signin(account_shorthand, password)
        sess_var_name = 'OP_SESSION_{}'.format(self.account_shorthand)
        # TODO: return alread-decoded token from sign-in
        env[sess_var_name] = self.token.decode()

    def _do_normal_signin(self, account_shorthand, password):
        self.logger.info("Doing normal (non-initial) 1Password sign-in")
        signin_argv = [self.op_path, "signin", "--output=raw"]

        if account_shorthand:
            signin_argv.extend(["--account", account_shorthand])

        token = self._run_signin(signin_argv, password=password).rstrip()
        return token

    @deprecated("Initial sign-in soon to be deprecated due to incompatibility with multi-factor authentication")
    def _do_initial_signin(self, account_shorthand, signin_address, email_address, secret_key, password):
        self.logger.info(
            "Performing initial 1Password sign-in to {} as {}".format(signin_address, email_address))
        signin_argv = [self.op_path, "signin", signin_address,
                       email_address, secret_key, "--output=raw"]
        if account_shorthand:
            signin_argv.extend(["--shorthand", account_shorthand])

        token = self._run_signin(signin_argv, password=password).rstrip()

        return token

    def _run_signin(self, argv, password=None):
        try:
            output = self._run(argv, capture_stdout=True,
                               input_string=password)
        except OPCmdFailedException as opfe:
            raise OPSigninException.from_opexception(opfe) from opfe

        return output

    @classmethod
    def _run(cls, argv, capture_stdout=False, input_string=None, decode=None):
        _ran = None
        stdout = subprocess.PIPE if capture_stdout else None
        if input_string:
            if isinstance(input_string, str):
                input_string = input_string.encode("utf-8")
        try:
            _ran = subprocess.run(argv, input=input_string,
                                  stderr=subprocess.PIPE, stdout=stdout, env=env)
        except FileNotFoundError as err:
            cls.logger.error(
                "1Password 'op' command not found at: {}".format(argv[0]))
            cls.logger.error(
                "See https://support.1password.com/command-line-getting-started/ for more information,")
            cls.logger.error(
                "or install from Homebrew with: 'brew install 1password-cli")
            raise OPNotFoundException(argv[0], err.errno) from err

        output = None
        try:
            _ran.check_returncode()
            if capture_stdout:
                output = _ran.stdout.decode(decode) if decode else _ran.stdout
        except subprocess.CalledProcessError as err:
            stderr_output = _ran.stderr.decode("utf-8").rstrip()
            returncode = _ran.returncode
            raise OPCmdFailedException(stderr_output, returncode) from err

        return output
