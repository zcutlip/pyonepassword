"""
Description: A module that maps methods to to `op` commands and subcommands
"""
import enum
import logging
from os import environ
from typing import Mapping, Optional, Union

from ._op_cli_argv import _OPArgv
from ._op_cli_config import OPCLIConfig
from ._py_op_cli import _OPCLIExecute
from .account import OPAccount, OPAccountList
from .op_cli_version import DOCUMENT_BYTES_BUG_VERSION, OPCLIVersion
from .py_op_exceptions import (
    OPCmdFailedException,
    OPDocumentDeleteException,
    OPDocumentGetException,
    OPGroupGetException,
    OPGroupListException,
    OPItemCreateException,
    OPItemDeleteException,
    OPItemGetException,
    OPItemListException,
    OPNotSignedInException,
    OPSigninException,
    OPUnknownAccountException,
    OPUserGetException,
    OPUserListException,
    OPVaultGetException,
    OPVaultListException
)


class ExistingAuthEnum(enum.IntEnum):
    IGNORE = 0     # Don't check if there's an existing authentication, peform new one regardless
    AVAILABLE = 1  # Check if there's an existing authentication, and if not, perform authentication
    REQUIRED = 2   # Check if there's an existing authentication, failing otherwise


EXISTING_AUTH_IGNORE = ExistingAuthEnum.IGNORE
EXISTING_AUTH_AVAIL = ExistingAuthEnum.AVAILABLE
EXISTING_AUTH_REQD = ExistingAuthEnum.REQUIRED


class _OPCommandInterface(_OPCLIExecute):
    """
    A class that directly maps methods to `op` commands
    & subcommands.
    No convenience methods are provided.
    No responses are parsed.
    """
    NOT_SIGNED_IN_TEXT = "not currently signed in"
    NO_ACTIVE_SESSION_FOUND_TEXT = "no active session found for account"
    NO_SESSION_TOKEN_FOUND_TEXT = "could not find session token for account"
    ACCT_IS_NOT_SIGNED_IN_TEXT = "account is not signed in"

    OP_PATH = 'op'  # let subprocess find 'op' in the system path

    def __init__(self,
                 account: str = None,
                 password: str = None,
                 existing_auth: ExistingAuthEnum = EXISTING_AUTH_IGNORE,
                 vault: str = None,
                 password_prompt: bool = True,
                 op_path: str = OP_PATH,
                 logger: logging.Logger = None):
        """
        Constructor to authenticate or verify existing authentication to `op`
        """
        super().__init__()
        if not logger:
            logger = logging.getLogger(self.__class__.__name__)
            logger.setLevel(logging.INFO)

        self.vault = vault
        self.logger = logger

        # Coerce existing_auth to an Enum in case it was passed in as a legacy bool
        # False -> ExistingAuthFlag.NONE, True -> ExistingAuthFlag.AVAILABLE
        existing_auth = ExistingAuthEnum(existing_auth)

        self.op_path = op_path
        self._account_identifier = account

        self._op_config: OPCLIConfig = None
        self._cli_version: OPCLIVersion = None
        self._account_list: OPAccountList = None
        self._uses_bio: bool = False
        self._sess_var: str = None

        # gathering facts will attempt to set the above instance variables
        # that got initialized to None or False
        self._gather_facts()

        # So far everything above has been fairly lightweight, with no remote
        # contact to the 1Password account.
        # The next steps will attempt to talk to the 1Password account, and
        # failing that, may attempt to authenticate to the 1Password account
        account_obj, token = self._new_or_existing_signin(
            existing_auth, password, password_prompt)
        self._signed_in_account: OPAccount = account_obj
        self._token = token
        if self._signed_in_account.is_service_account():
            self.logger.debug("Signed in as a service account")
        else:
            self.logger.debug(
                f"Signed in as User ID: {self._signed_in_account.user_uuid}")
        # export OP_SESSION_<use_id>
        if self.token:
            if not self._account_identifier:
                # if we weren't provided an account identifier,
                # we can now get it from the signed-in account object
                # and compute the session environment variable name
                self._account_identifier = account_obj.user_uuid
                self._sess_var = self._compute_session_var_name()
            environ[self._sess_var] = self.token

    @property
    def token(self) -> str:
        return self._token

    @property
    def session_var(self) -> str:
        return self._sess_var

    @classmethod
    def uses_biometric(cls, op_path: str = "op", encoding: str = "utf-8", account_list: OPAccountList = None):
        uses_bio = True
        # We can run 'op account list', which doesn't require talking (or authenticating)
        # to the 1Password account
        # if biometric is enabled, there will be no account shorthands in the output
        # if there are account shorthands, biometric is not enabled
        if account_list is None:
            account_list = cls._get_account_list(op_path, decode=encoding)
        acct: OPAccount
        for acct in account_list:
            if not acct.shorthand:
                continue
            # There is at least one account_shorthand found in `op account list`
            uses_bio = False
            break
        return uses_bio

    def _gather_facts(self):
        self._op_config = OPCLIConfig()
        self._cli_version = self._get_cli_version(self.op_path)
        self._account_list = self._get_account_list(self.op_path)
        self._uses_bio = self.uses_biometric(
            op_path=self.op_path, account_list=self._account_list)
        self._account_identifier = self._normalize_account_id()
        self._sess_var = self._compute_session_var_name()

    def _get_cli_version(self, op_path: str) -> OPCLIVersion:
        argv = _OPArgv.cli_version_argv(op_path)
        output = self._run(argv, capture_stdout=True, decode="utf-8")
        output = output.rstrip()
        cli_version = OPCLIVersion(output)
        return cli_version

    @classmethod
    def _get_account_list(cls, op_path, decode="utf-8") -> OPAccountList:
        account_list_json = cls._signed_in_accounts(op_path, decode=decode)
        account_list = OPAccountList(account_list_json)
        return account_list

    def _normalize_account_id(self):
        # we need to turn whatever we were given into a User ID
        # we could have been given any of the following for account ID:
        # - None
        # - account shorthand
        # - account URL
        # - account UUID
        # - user UUID
        # see: 'op --help' for '--account' global flag
        user_uuid = None
        if not self._uses_bio:
            if self._account_identifier:
                # if we were given an specific account look up user ID for that
                user_uuid = self._op_config.uuid_for_account(
                    self._account_identifier)
            else:
                # else try to look up User ID for latest sign-in
                # (may come back None)
                user_uuid = self._op_config.latest_signin_uuid
        elif self._account_identifier:
            user_uuid = self._account_list.user_id_for_account_identifier(
                self._account_identifier)

        if self._account_identifier and not user_uuid:
            raise OPUnknownAccountException(
                f"No account found for identifier: {self._account_identifier}")

        return user_uuid

    def _compute_session_var_name(self):
        sess_var_name = self._sess_var
        # normalize account identifier before calling this
        user_uuid = self._account_identifier

        # we can only use a session variable if:
        #   - biometric isn't enabled, and
        #   - we have an account shorthand

        if user_uuid and not self._uses_bio:
            sess_var_name = 'OP_SESSION_{}'.format(user_uuid)
        return sess_var_name

    def _new_or_existing_signin(self, existing_auth: ExistingAuthEnum, password: str, password_prompt: bool):
        token = None
        account = None

        # Don't attempt to verify sign-in unless caller told us to
        # otherwise it will trigger a prompt, either GUI biometric prompt,
        # or interactive console prompt
        if existing_auth in [EXISTING_AUTH_AVAIL, EXISTING_AUTH_REQD]:
            account = self._verify_signin()

        if account:
            token = self._get_existing_token(account)
        else:
            if existing_auth == EXISTING_AUTH_REQD:
                # we were told to only use existing authentication but verificaiton failed
                # this is a hard error
                raise OPNotSignedInException(
                    "Existing authentication specified as required, but could not be verified.")

            # we couldn't verify being signed in (or weren't told to try)
            # let's try a normal sign-in
            # _do_normal_signin() will raise OPNotSignedInException if
            # _uses_bio is false, no password given, and password prompt not allowed
            token = self._do_normal_signin(password, password_prompt)
            account = self._verify_signin(token=token)
        return (account, token)

    def _verify_signin(self, token: str = None):
        env: Mapping
        account = None
        if token and self._sess_var:
            # we need to pass an environment dictionary to subprocess.run() that contains
            # the session token we're trying to verify
            #
            # make a copy of environment rather than modifying actual env
            # in order to verify login
            # we'll offically set it once we know it works
            env = dict(environ)
            env[self._sess_var] = token
        else:
            # we don't have a token to verify
            # so no need to modify or copy the environment
            # we can use it as-is
            env = environ

        # this step actually talks to the 1Password account
        # it uses "op whoami" which is a very non-intrusive
        # query that will fail without authentication
        argv = _OPArgv.whoami_argv(
            self.op_path, account=self._account_identifier)
        try:
            account_json = self._run(
                argv, capture_stdout=True, decode="utf-8", env=env)
            account = OPAccount(account_json)
        except OPCmdFailedException as opfe:
            # scrape error message about not being signed in

            fragments = [self.NO_ACTIVE_SESSION_FOUND_TEXT,
                         self.NOT_SIGNED_IN_TEXT,
                         self.NO_SESSION_TOKEN_FOUND_TEXT,
                         self.ACCT_IS_NOT_SIGNED_IN_TEXT]
            unknown_err = True
            for frag in fragments:
                if frag in opfe.err_output:
                    unknown_err = False
                    break
            # there was a different error so raise the exception
            if unknown_err:  # pragma: no cover
                raise opfe

        return account

    def _do_normal_signin(self, password: str, password_prompt: bool) -> Union[str, None]:
        # normalize empty string to None, otherwise use password as given
        password = None if password == "" else password

        # there are three things that can be used for a *new* authentication:
        # - biometric
        # - password
        # - allow 'op' to interactively prompt
        # NOTE: we need to keep this check as close to the call to _run_signin() as possible
        #       We can't tell 'op' not to prompt. We just have to not run it if we're not prompting
        if not self._uses_bio and not password and not password_prompt:
            # - we weren't provided a password, and
            # - we were told not to let 'op' prompt for a password, and
            # - biometric is not enabled
            # so we can't sign in
            raise OPNotSignedInException(
                "No existing session and no password provided.")
        signin_argv = _OPArgv.normal_signin_argv(
            self.op_path, account=self._account_identifier)

        token = self._run_signin(signin_argv, password=password)
        if self._uses_bio:
            # Set to None vs empty string
            token = None

        return token

    def _get_existing_token(self, account: OPAccount):
        if self._sess_var:
            token = environ.get(self._sess_var)
        else:
            token = None
        return token

    def _run_signin(self, argv, password=None):
        try:
            output = self._run(argv, capture_stdout=True,
                               input_string=password, decode="utf-8")
        except OPCmdFailedException as opfe:
            raise OPSigninException.from_opexception(opfe) from opfe

        return output

    @classmethod
    def _account_list_argv(cls, op_path="op", encoding="utf-8"):
        argv = _OPArgv.account_list_argv(op_path, encoding=encoding)
        return argv

    def _item_get_argv(self, item_name_or_id, vault=None, fields=None, include_archive=False):
        vault_arg = vault if vault else self.vault

        lookup_argv = _OPArgv.item_get_argv(
            self.op_path, item_name_or_id, vault=vault_arg, fields=fields, include_archive=include_archive)
        return lookup_argv

    def _item_delete_argv(self, item_name_or_id, vault=None, archive=False):
        vault_arg = vault if vault else self.vault

        delete_argv = _OPArgv.item_delete_argv(
            self.op_path, item_name_or_id, vault=vault_arg, archive=archive)
        return delete_argv

    def _item_get_totp_argv(self, item_name_or_id, vault=None):
        vault_arg = vault if vault else self.vault

        lookup_argv = _OPArgv.item_get_totp_argv(
            self.op_path, item_name_or_id, vault=vault_arg)
        return lookup_argv

    def _document_get_argv(self,
                           document_name_or_id: str,
                           vault: Optional[str] = None,
                           include_archive: Optional[bool] = False):
        vault_arg = vault if vault else self.vault
        document_get_argv = _OPArgv.document_get_argv(self.op_path,
                                                      document_name_or_id,
                                                      vault=vault_arg,
                                                      include_archive=include_archive)
        print(document_get_argv)

        return document_get_argv

    def _document_delete_argv(self, document_name_or_id: str, vault: Optional[str] = None, archive=False):
        vault_arg = vault if vault else self.vault

        document_delete_argv = _OPArgv.document_delete_argv(
            self.op_path, document_name_or_id, vault=vault_arg, archive=archive)

        return document_delete_argv

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

    def _item_get(self, item_name_or_id, vault=None, fields=None, include_archive=False, decode="utf-8"):
        get_item_argv = self._item_get_argv(
            item_name_or_id, vault=vault, fields=fields, include_archive=include_archive)
        try:
            output = self._run(
                get_item_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPItemGetException.from_opexception(ocfe) from ocfe

        return output

    def _item_delete(self, item_name_or_id, vault=None, archive=False, decode="utf-8"):
        item_delete_argv = self._item_delete_argv(
            item_name_or_id, vault=vault, archive=archive)
        try:
            # 'op item delete' doesn't have any output if successful
            # if it fails, stderr will be in the exception object
            self._run(item_delete_argv, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPItemDeleteException.from_opexception(ocfe)

        return

    def _item_get_totp(self, item_name_or_id, vault=None, decode="utf-8"):
        item_get_totp_argv = self._item_get_totp_argv(
            item_name_or_id, vault=vault)
        try:
            output = self._run(
                item_get_totp_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPItemGetException.from_opexception(ocfe) from ocfe

        return output

    def _document_get(self,
                      document_name_or_id: str,
                      vault: Optional[str] = None,
                      include_archive: Optional[bool] = False):
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

        get_document_argv = self._document_get_argv(
            document_name_or_id, vault=vault, include_archive=include_archive)

        try:
            document_bytes = self._run(get_document_argv, capture_stdout=True)
        except OPCmdFailedException as ocfe:
            raise OPDocumentGetException.from_opexception(ocfe) from ocfe

        if self._cli_version <= DOCUMENT_BYTES_BUG_VERSION:  # pragma: no cover
            # op v2.x appends an erroneous \x0a ('\n') byte to document bytes
            # trim it off if its present
            if document_bytes[-1] == 0x0a:
                document_bytes = document_bytes[:-1]

        return document_bytes

    def _document_delete(self, document_name_or_id: str, vault: Optional[str] = None, archive=False):

        document_delete_argv = self._document_delete_argv(
            document_name_or_id, vault=vault, archive=archive)
        try:
            # 'op document delete' doesn't have any output if successful
            # if it fails, stderr will be in the exception object
            self._run(document_delete_argv)
        except OPCmdFailedException as ocfe:
            raise OPDocumentDeleteException.from_opexception(ocfe)

        return

    @classmethod
    def _signed_in_accounts(cls, op_path, decode="utf-8"):
        account_list_argv = cls._account_list_argv(op_path, encoding=decode)
        output = cls._run(account_list_argv,
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

    def _signout(self, account, session, forget=False):   # pragma: no cover
        if forget and self._uses_bio:
            self.logger.warn(
                "Biometric is enabled. 'forget' operation will have no effect.")
        argv = _OPArgv.signout_argv(
            self.op_path, account, session, forget=forget, uses_bio=self._uses_bio)
        self._run(argv)

    @classmethod
    def _forget(cls, account: str, op_path=None):   # pragma: no cover
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

    def _item_create_argv(self, item, password_recipe, vault):
        vault_arg = vault if vault else self.vault
        create_item_argv = _OPArgv.item_create_argv(
            self.op_path, item, password_recipe=password_recipe, vault=vault_arg
        )
        return create_item_argv

    def _item_create(self, item, vault, password_recipe, decode="utf-8"):
        argv = self._item_create_argv(item, password_recipe, vault)
        try:
            output = self._run(argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as e:
            raise OPItemCreateException.from_opexception(e)

        return output
