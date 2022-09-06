"""
Description: A module that maps methods to to `op` commands and subcommands
"""
import logging
from os import environ as env

from ._op_cli_argv import _OPArgv
from ._op_cli_config import OPCLIConfig
from ._py_op_cli import _OPCLIExecute
from .account import OPAccount, OPAccountList
from .op_cli_version import DOCUMENT_BYTES_BUG_VERSION, OPCLIVersion
from .op_objects import OPUser
from .py_op_exceptions import (
    OPCmdFailedException,
    OPDocumentGetException,
    OPGroupGetException,
    OPGroupListException,
    OPItemGetException,
    OPItemListException,
    OPNotSignedInException,
    OPSigninException,
    OPUserGetException,
    OPUserListException,
    OPVaultGetException,
    OPVaultListException
)


class _OPCommandInterface(_OPCLIExecute):
    """
    A class that directly maps methods to `op` commands
    & subcommands.
    No convenience methods are provided.
    No responses are parsed.
    """

    OP_PATH = 'op'  # let subprocess find 'op' in the system path

    def __init__(self,
                 vault=None,
                 account_shorthand=None,
                 password=None,
                 logger=None,
                 op_path='op',
                 existing_auth=False,
                 password_prompt=True):
        """
        Create an OP object. The 1Password sign-in happens during object instantiation.
        If 'password' is not provided, the 'op' command will prompt on the console for a password.

        Arguments:
            - 'account_shorthand': The shorthand name for the account on this device.
                                   See 'op signin --help' for more information.
            - 'password': The user's master password
            - 'logger': A logging object. If not provided a basic logger is created and used.
            - 'op_path': optional path to the `op` command, if it's not at the default location

        Raises:
            - OPSigninException if 1Password sign-in fails for any reason.
            - OPNotFoundException if the 1Password command can't be found.
        """
        super().__init__()
        self.vault = vault
        if not logger:
            logging.basicConfig(format="%(message)s", level=logging.DEBUG)
            logger = logging.getLogger()
        self.logger = logger
        self.op_path = op_path

        self._op_config: OPCLIConfig = None
        self._cli_version: OPCLIVersion = None
        self._uses_bio: bool = False
        self._account_shorthand: str = None
        self._sess_var: str = None

        # gathering facts will attempt to set the above instance variables
        # that got initialized to None or False
        self._gather_facts(account_shorthand)

        # So far everything above has been fairly lightweight, with no remote
        # contact to the 1Password account.
        # The next steps will attempt to talk to the 1Password account, and
        # failing that, may attempt to authenticate to the 1Password account
        user, token = self._new_or_existing_signin(
            existing_auth, password, password_prompt)
        self._signed_in_user: OPUser = user
        self._token = token
        self.logger.debug(
            f"Signed in as User ID: {self._signed_in_user.unique_id}")
        # export OP_SESSION_<signin_address>
        if self._sess_var and self.token:
            env[self._sess_var] = self.token

    @property
    def token(self) -> str:
        return self._token

    @property
    def session_var(self) -> str:
        return self._sess_var

    @classmethod
    def uses_biometric(cls, op_path="op", account_shorthand=None, encoding="utf-8"):
        uses_bio = True
        # We can run 'op account list', which doesn't require talking (or authenticating)
        # to the 1Password account
        # if biometric is enabled, there will be no account shorthands in the output
        # if there are account shorthands, biometric is not enabled
        account_list_argv = cls._account_list_argv(
            op_path=op_path, encoding=encoding)
        account_list_json = cls._run(
            account_list_argv, capture_stdout=True, decode=encoding)
        account_list = OPAccountList(account_list_json)
        acct: OPAccount
        for acct in account_list:
            if not acct.shorthand:
                continue
            if account_shorthand:
                if acct.shorthand != account_shorthand:
                    continue
            # There is at least one account_shorthand found in `op account list`
            # and if we were given a specific shorthand to use, it matches
            uses_bio = False
            break
        return uses_bio

    def _gather_facts(self, account_shorthand):
        self._op_config = OPCLIConfig()
        self._cli_version: OPCLIVersion = self._get_cli_version(self.op_path)
        self._uses_bio = self.uses_biometric(
            self.op_path, account_shorthand=account_shorthand)

        if account_shorthand is None:
            account_shorthand = self._get_account_shorthand()
        self._account_shorthand = account_shorthand
        self._sess_var = self._compute_session_var_name()

    def _get_cli_version(self, op_path):
        argv = _OPArgv.cli_version_argv(op_path)
        output = self._run(argv, capture_stdout=True, decode="utf-8")
        output = output.rstrip()
        cli_version = OPCLIVersion(output)
        return cli_version

    def _get_account_shorthand(self):
        account_shorthand = None
        if not self._uses_bio:
            try:
                account_shorthand = self._op_config.latest_signin
                self.logger.debug(
                    "Using account shorthand found in op config: {}".format(account_shorthand))
            except KeyError:
                pass
        return account_shorthand

    def _compute_session_var_name(self):
        sess_var_name = None
        # we can only use a session variable if:
        #   - biomatric isn't enabled, and
        #   - we have an account shorthand
        if not self._uses_bio and self._account_shorthand:
            user_uuid = self._op_config.uuid_for_shorthand(
                self._account_shorthand)
            sess_var_name = 'OP_SESSION_{}'.format(user_uuid)
        return sess_var_name

    def _new_or_existing_signin(self, existing_auth: bool, password: str, password_prompt: bool):
        token = None
        user = self._verify_signin(existing_auth)

        if not user:
            # If we couldn't verify being signed in. we need to authenticate
            # there are three things that can be used for a new authentication:
            # - biometric
            # - password
            # - allow 'op' to interactively prompt
            if not self._uses_bio and not password and not password_prompt:
                # we need to authenticate, but don't have at least one of the three options
                # so not being signed in is an error
                raise OPNotSignedInException(
                    "No existing authentication, biometric not enabled, and no password provided.")
            # we couldn't verify being signed in (or weren't told to try)
            # let's try a normal sign-in
            token = self._do_normal_signin(password, password_prompt)
            user = self._verify_signin(False)
        return (user, token)

    def _verify_signin(self, existing_auth):
        user: OPUser = None

        # this step actually talks to the 1Password account
        # it uses "op user get --me" which is a very non-intrusive
        # query that will fail without authentication
        argv = _OPArgv.user_get_signed_in_argv(self.op_path)
        try:
            user_json = self._run(argv, capture_stdout=True, decode="utf-8")
            self.logger.info(f"user_json: {user_json}")
            user = OPUser(user_json)
        except OPCmdFailedException as opfe:
            # scrape error message about not being signed in
            if self.NOT_SIGNED_IN_TEXT not in opfe.err_output:
                # there was a different error so raise the exception
                raise opfe

        return user

    def _do_normal_signin(self, password: str, password_prompt: bool):
        if not self._uses_bio and not password and not password_prompt:
            # - we weren't provided a password, and
            # - we were told not to let 'op' prompt for a password, and
            # - biometric is not enabled
            raise OPNotSignedInException(
                "No existing session and no password provided.")
        signin_argv = _OPArgv.normal_signin_argv(
            self.op_path, account=self._account_shorthand)

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
    def _account_list_argv(cls, op_path="op", encoding="utf-8"):
        argv = _OPArgv.account_list_argv(op_path, encoding=encoding)
        return argv

    def _item_get_argv(self, item_name_or_id, vault=None, fields=None):
        vault_arg = vault if vault else self.vault

        lookup_argv = _OPArgv.item_get_argv(
            self.op_path, item_name_or_id, vault=vault_arg, fields=fields)
        return lookup_argv

    def _item_get_totp_argv(self, item_name_or_id, vault=None):
        vault_arg = vault if vault else self.vault

        lookup_argv = _OPArgv.item_get_totp_argv(
            self.op_path, item_name_or_id, vault=vault_arg)
        return lookup_argv

    def _get_document_argv(self, document_name_or_id: str, vault: str = None):
        vault_arg = vault if vault else self.vault

        get_document_argv = _OPArgv.document_get_argv(
            self.op_path, document_name_or_id, vault=vault_arg)

        return get_document_argv

    def _user_get_argv(self, user_name_or_id: str):
        get_user_argv = _OPArgv.user_get_argv(self.op_path, user_name_or_id)
        return get_user_argv

    def _user_list_argv(self, group_name_or_id=None, vault=None):
        user_list_argv = _OPArgv.user_list_argv(
            self.op_path, group_name_or_id=group_name_or_id, vault=vault)
        return user_list_argv

    def _group_get_argv(self, group_name_or_id: str):
        group_get_argv = _OPArgv.group_get_argv(
            self.op_path, group_name_or_id)
        return group_get_argv

    def _group_list_argv(self, user_name_or_id=None, vault=None):
        group_list_argv = _OPArgv.group_list_argv(
            self.op_path, user_name_or_id=user_name_or_id, vault=vault)
        return group_list_argv

    def _vault_get_argv(self, vault_name_or_id: str):

        get_vault_argv = _OPArgv.vault_get_argv(
            self.op_path, vault_name_or_id)
        return get_vault_argv

    def _vault_list_argv(self, group_name_or_id=None, user_name_or_id=None):
        vault_list_argv = _OPArgv.vault_list_argv(
            self.op_path, group_name_or_id=group_name_or_id, user_name_or_id=user_name_or_id)
        return vault_list_argv

    def _cli_version_argv(self):
        # Specifically for use by mock_op response-generator
        cli_version_argv = _OPArgv.cli_version_argv(self.op_path)
        return cli_version_argv

    def _item_get(self, item_name_or_id, vault=None, fields=None, decode="utf-8"):
        get_item_argv = self._item_get_argv(
            item_name_or_id, vault=vault, fields=fields)
        try:
            output = self._run(
                get_item_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPItemGetException.from_opexception(ocfe) from ocfe

        return output

    def _item_get_totp(self, item_name_or_id, vault=None, decode="utf-8"):
        item_get_totp_argv = self._item_get_totp_argv(
            item_name_or_id, vault=vault)
        try:
            output = self._run(
                item_get_totp_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPItemGetException.from_opexception(ocfe) from ocfe

        return output

    def _document_get(self, document_name_or_id: str, vault: str = None):
        """
        Download a document object from a 1Password vault by name or UUID.

        Arguments:
            - 'item_name_or_id': The item to look up
        Raises:
            - OPDocumentGetException if the lookup fails for any reason.
            - OPNotFoundException if the 1Password command can't be found.
        Returns:
            - Bytes: document bytes
        """

        get_document_argv = self._get_document_argv(
            document_name_or_id, vault=vault)

        try:
            document_bytes = self._run(get_document_argv, capture_stdout=True)
        except OPCmdFailedException as ocfe:
            raise OPDocumentGetException.from_opexception(ocfe) from ocfe

        if self._cli_version <= DOCUMENT_BYTES_BUG_VERSION:
            # op v2.x appends an erroneous \x0a ('\n') byte to document bytes
            # trim it off if its present
            if document_bytes[-1] == 0x0a:
                document_bytes = document_bytes[:-1]
        else:
            print(self._cli_version)
        return document_bytes

    def _signed_in_accounts(self, decode="utf-8"):
        account_list_argv = self._account_list_argv(op_path=self.op_path)
        output = self._run(account_list_argv,
                           capture_stdout=True, decode=decode)
        return output

    def _user_get(self, user_name_or_id: str, decode: str = "utf-8") -> str:
        get_user_argv = self._user_get_argv(user_name_or_id)
        try:
            output = self._run(
                get_user_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPUserGetException.from_opexception(ocfe) from ocfe
        return output

    def _user_list(self, group_name_or_id=None, vault=None, decode: str = "utf-8") -> str:
        user_list_argv = self._user_list_argv(
            group_name_or_id=group_name_or_id, vault=vault)
        try:
            output = self._run(
                user_list_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPUserListException.from_opexception(ocfe)
        return output

    def _group_get(self, group_name_or_id: str, decode: str = "utf-8") -> str:
        group_get_argv = self._group_get_argv(group_name_or_id)
        try:
            output = self._run(
                group_get_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPGroupGetException.from_opexception(ocfe) from ocfe
        return output

    def _group_list(self, user_name_or_id=None, vault=None, decode: str = "utf-8") -> str:
        group_list_argv = self._group_list_argv(
            user_name_or_id=user_name_or_id, vault=vault)
        try:
            output = self._run(
                group_list_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPGroupListException.from_opexception(ocfe)
        return output

    def _vault_get(self, vault_name_or_id: str, decode: str = "utf-8") -> str:
        vault_get_argv = self._vault_get_argv(vault_name_or_id)
        try:
            output = self._run(
                vault_get_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPVaultGetException.from_opexception(ocfe)
        return output

    def _vault_list(self, group_name_or_id=None, user_name_or_id=None, decode="utf-8") -> str:
        vault_list_argv = self._vault_list_argv(
            group_name_or_id=group_name_or_id, user_name_or_id=user_name_or_id)
        try:
            output = self._run(
                vault_list_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPVaultListException.from_opexception(ocfe)
        return output

    def _signout(self, account, session, forget=False):
        if forget and self._uses_bio:
            self.logger.warn(
                "Biometric is enabled. 'forget' operation will have no effect.")
        argv = _OPArgv.signout_argv(
            self.op_path, account, session, forget=forget, uses_bio=self._uses_bio)
        self._run(argv)

    @classmethod
    def _forget(cls, account: str, op_path=None):
        if not op_path:
            op_path = cls.OP_PATH
        argv = _OPArgv.forget_argv(op_path, account)
        cls._run(argv)

    def _item_list_argv(self, categories=[], include_archive=False, tags=[], vault=None):
        vault_arg = vault if vault else self.vault
        list_items_argv = _OPArgv.item_list_argv(self.op_path,
                                                 categories=categories, include_archive=include_archive, tags=tags, vault=vault_arg)
        return list_items_argv

    def _item_list(self, categories=[], include_archive=False, tags=[], vault=None, decode="utf-8"):
        argv = self._item_list_argv(
            categories=categories, include_archive=include_archive, tags=tags, vault=vault)
        try:
            output = self._run(argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as e:
            raise OPItemListException.from_opexception(e)
        return output
