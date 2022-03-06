import logging
from os import environ as env

from .._argv_generator import OPArgvGenerator
from .._op_cli_config import OPCLIConfig
from .._py_op_deprecation import deprecated
from ..op_cli import OPArgvCommon, _OPCLIExecute
from ..op_cli_version import MINIMUM_VERSION_2
from ..op_items._op_items_base import OPAbstractItem
from ..py_op_exceptions import (
    OPCmdFailedException,
    OPNotSignedInException,
    OPSigninException
)
from ._op_commands_abstract import (
    _OPCommandInterfaceAbstract,
    _OPCommandRegistry
)


class _OPCommandInterface(_OPCommandInterfaceAbstract, metaclass=_OPCommandRegistry):
    MIN_CLI_VERSION = None
    MAX_CLI_VERSION = None

    OP_PATH = 'op'  # let subprocess find 'op' in the system path

    def __init__(self,
                 vault=None,
                 account_shorthand=None,
                 signin_address=None,
                 email_address=None,
                 secret_key=None,
                 password=None,
                 logger=None,
                 op_path_or_exe='op',
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
        if isinstance(op_path_or_exe, str):
            self._op_exe = _OPCLIExecute(op_path_or_exe)
        else:
            self._op_exe = op_path_or_exe
        self.vault = vault
        self._argv_generator = OPArgvGenerator(self.cli_version)
        op_cmd_class = _OPCommandRegistry.op_command_class(self.cli_version)

        if logger:
            self.logger = logger
        else:
            logging.basicConfig(format="%(message)s", level=logging.DEBUG)
            self.logger = logging.getLogger()

        self._op_cmd_impl: _OPCommandInterfaceAbstract = op_cmd_class(
            self._op_exe, vault=vault, logger=self.logger)

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
                if MINIMUM_VERSION_2 <= self.cli_version:
                    raise NotImplementedError(
                        "Initial sign-in not implemented for 'op' verisons 2.0 & greater")
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

    def _verify_signin(self, sess_var_name):
        # Need to get existing token if we're already signed in
        token = env.get(sess_var_name)

        if token:
            # if there's no token, no need to sign in
            argv = self._argv_generator.get_verify_signin_argv(self._op_exe)
            try:
                self._op_exe._run(argv, capture_stdout=True)
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
        signin_argv = self._argv_generator.normal_signin_argv(
            self._op_exe, account_shorthand=account_shorthand)

        token = self._run_signin(signin_argv, password=password).rstrip()
        return token.decode()

    @deprecated("Initial sign-in soon to be deprecated due to incompatibility with multi-factor authentication")
    def _do_initial_signin(self, account_shorthand, signin_address, email_address, secret_key, password):
        self.logger.info(
            "Performing initial 1Password sign-in to {} as {}".format(signin_address, email_address))
        signin_argv = [self._op_exe, "signin", signin_address,
                       email_address, secret_key, "--raw"]
        if account_shorthand:
            signin_argv.extend(["--shorthand", account_shorthand])

        token = self._run_signin(signin_argv, password=password).rstrip()

        return token.decode()

    def _run_signin(self, argv, password=None):
        try:
            output = self._op_exe._run(argv, capture_stdout=True,
                                       input_string=password)
        except OPCmdFailedException as opfe:
            raise OPSigninException.from_opexception(opfe) from opfe

        return output

    def _set_op_exe(self, op_path):
        if not hasattr(self, "_op_exe"):
            op_exe = op_path
            if isinstance(op_path, str):
                op_exe = _OPCLIExecute(op_path)
            self._op_exe = op_exe

    def supports_item_creation(self) -> bool:
        return self._op_cmd_impl.supports_item_creation()

    def _get_item_argv(self,
                       item_name_or_uuid,
                       vault=None,
                       fields=None) -> OPArgvCommon:
        return self._op_cmd_impl._get_item_argv(item_name_or_uuid, vault, fields)

    def _get_totp_argv(self, item_name_or_uuid, vault=None):
        return self._op_cmd_impl._get_totp_argv(item_name_or_uuid, vault)

    def _get_document_argv(self, document_name_or_uuid: str, vault: str = None):
        return self._op_cmd_impl._get_document_argv(document_name_or_uuid, vault)

    def _get_user_argv(self, user_name_or_uuid: str):
        return self._op_cmd_impl._get_user_argv(user_name_or_uuid)

    def _get_group_argv(self, group_name_or_uuid: str):
        return self._op_cmd_impl._get_group_argv(group_name_or_uuid)

    def _get_vault_argv(self, vault_name_or_uuid: str):
        return self._op_cmd_impl._get_vault_argv(vault_name_or_uuid)

    def _get_item(self, item_name_or_uuid, vault=None, fields=None, decode="utf-8"):
        impl = self._op_cmd_impl
        item = impl._get_item(item_name_or_uuid, vault=vault,
                              fields=fields, decode=decode)
        return item

    def _get_totp(self, item_name_or_uuid, vault=None, decode="utf-8"):
        return self._op_cmd_impl._get_totp(item_name_or_uuid, vault, decode)

    def _get_document(self, document_name_or_uuid: str, vault: str = None):
        return self._op_cmd_impl._get_document(document_name_or_uuid, vault)

    def _get_user(self, user_name_or_uuid: str, decode: str = "utf-8") -> str:
        return self._op_cmd_impl._get_user(user_name_or_uuid, decode)

    def _get_group(self, group_name_or_uuid: str, decode: str = "utf-8") -> str:
        return self._op_cmd_impl._get_group(group_name_or_uuid, decode)

    def _get_vault(self, vault_name_or_uuid: str, decode: str = "utf-8") -> str:
        return self._op_cmd_impl._get_vault(vault_name_or_uuid, decode)

    def _create_item(self, item: OPAbstractItem, item_name, vault=None):
        return self._op_cmd_impl._create_item(item, item_name, vault)

    def _signout(self, account, session, forget=False):
        return self._op_cmd_impl._signout(account, session, forget)

    @classmethod
    def _forget(cls, account: str, op_path='op'):
        op_exe = _OPCLIExecute(op_path)
        cli_version = op_exe.cli_version
        op_impl: _OPCommandInterfaceAbstract = _OPCommandRegistry.op_command_class(
            cli_version)

        return op_impl._forget(account, op_path=op_path)

    def _create_item_argv(self, item, item_name, vault):
        return self._create_item_argv(item, item_name, vault)

    def _list_items_argv(self, categories=[], include_archive=False, tags=[], vault=None):
        return self._list_items_argv(categories, include_archive, tags, vault)

    def _list_items(self, categories=[], include_archive=False, tags=[], vault=None, decode="utf-8"):
        return self._list_items(categories, include_archive, tags, vault, decode)
