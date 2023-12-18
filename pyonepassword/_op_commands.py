"""
Description: A module that maps methods to to `op` commands and subcommands
"""
from __future__ import annotations

import enum
import logging
from os import environ
from typing import TYPE_CHECKING, Dict, List, Mapping, Optional, Union

if TYPE_CHECKING:  # pragma: no coverage
    from pyonepassword._field_assignment import OPFieldTypeEnum

from ._op_cli import _OPCLIExecute
from ._op_cli_argv import _OPArgv
from ._op_cli_config import OPCLIConfig
from ._svc_account import (
    SVC_ACCT_CMD_NOT_SUPPORTED,
    SVC_ACCT_INCOMPAT_OPTIONS,
    SVC_ACCT_SUPPORTED,
    OPSvcAcctCommandNotSupportedException
)
from .account import OPAccount, OPAccountList
from .op_cli_version import (
    DOCUMENT_BYTES_BUG_VERSION,
    MINIMUM_SERVICE_ACCOUNT_VERSION,
    OPCLIVersion
)
from .op_items.password_recipe import OPPasswordRecipe
from .py_op_exceptions import (
    OPAuthenticationException,
    OPCmdFailedException,
    OPCmdMalformedSvcAcctTokenException,
    OPDocumentDeleteException,
    OPDocumentEditException,
    OPDocumentGetException,
    OPGroupGetException,
    OPGroupListException,
    OPItemCreateException,
    OPItemDeleteException,
    OPItemEditException,
    OPItemGetException,
    OPItemListException,
    OPSigninException,
    OPUnknownAccountException,
    OPUserEditException,
    OPUserGetException,
    OPUserListException,
    OPVaultGetException,
    OPVaultListException,
    OPWhoAmiException
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
    SVC_ACCT_TOKEN_MALFORMED_TEXT = "failed to DecodeSACCredentials"
    SVC_ACCT_TOKEN_NOT_AUTH_TXT = "service account token set, but not authenticated yet"

    OP_SVC_ACCOUNT_ENV_VAR = "OP_SERVICE_ACCOUNT_TOKEN"
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
        self.op_path = op_path
        self._account_identifier = account
        self._signed_in_account: OPAccount = None

        self._cli_version: OPCLIVersion
        self._op_config: OPCLIConfig = None
        self._account_list: OPAccountList = None
        self._uses_bio: bool = False
        self._sess_var: str = None
        # gathering facts will attempt to set the above instance variables
        # that got initialized to None or False
        self._gather_facts()

        # part of exception message in case incompatible authentication parameters
        # are provided
        auth_pref_source = "preference passed as argument"
        if self.svc_account_env_var_set():
            # - 'op' won't prompt for authentication of OP_SERVICE_ACCOUNT_TOKEN is set
            # - Even if we explicitly call signin and succeed, it ignores that authentication
            # so we need to suppress any path that tries to or expects to authenticate
            if self._cli_version < MINIMUM_SERVICE_ACCOUNT_VERSION:
                raise OPAuthenticationException(
                    f"Version {self._cli_version} not supported with service accounts. Minimum version: {MINIMUM_SERVICE_ACCOUNT_VERSION}")
            if existing_auth != EXISTING_AUTH_REQD:
                auth_pref_source = "preference upgraded due to service account environment variable"
                self.logger.info(
                    f"{self.OP_SVC_ACCOUNT_ENV_VAR} was set. Upgrading existing auth flag to REQUIRED")
                existing_auth = EXISTING_AUTH_REQD

        if existing_auth == EXISTING_AUTH_REQD and password is not None:
            # if a password is passed in but existing_auth is required, caller may be confused:
            # - intentionally passed in incompatible options
            # - possibly has OP_SERVICE_ACCOUNT_TOKEN set accidentally
            msg = f"Password argument passed but EXISTING_AUTH_REQD flag is set. flag source: {auth_pref_source}"
            self.logger.error(msg)
            raise OPAuthenticationException(msg)

        # So far everything above has been fairly lightweight, with no remote
        # contact to the 1Password account.
        # The next steps will attempt to talk to the 1Password account, and
        # failing that, may attempt to authenticate to the 1Password account
        account_obj, token = self._new_or_existing_signin(
            existing_auth, password, password_prompt)
        self._signed_in_account = account_obj
        self._token = token
        if self._signed_in_account.is_service_account():
            self.logger.debug("Signed in as a service account")
        else:
            self.logger.debug(
                f"Signed in as User ID: {self._signed_in_account.sanitized_user_uuid}")
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
    def svc_account_env_var_set(cls):
        svc_acct_set = False
        if environ.get(cls.OP_SVC_ACCOUNT_ENV_VAR):
            svc_acct_set = True
        return svc_acct_set

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
                raise OPAuthenticationException(
                    "Existing authentication specified as required, but could not be verified.")

            # we couldn't verify being signed in (or weren't told to try)
            # let's try a normal sign-in
            # _do_normal_signin() will raise OPAuthenticationException if
            # _uses_bio is false, no password given, and password prompt not allowed
            token = self._do_normal_signin(password, password_prompt)
            account = self._verify_signin(token=token)
        return (account, token)

    @classmethod
    def _auth_expired(cls, op_path, account):
        # this is a test to see if the previously valid authentication
        # is still valid, with the assumption that if it is not, then it
        # has expired
        # it is primarily for the following two purposes
        # - avoid triggering an interactive prompt or GUI dialogue (if undesired) and hanging indefinitely
        # - being able to raise OPAuthenticationException to the caller rather than a generic
        #   "command failed" exception
        expired = False

        try:
            cls._whoami(op_path, account=account)
        except OPWhoAmiException:  # pragma: no cover
            expired = True

        return expired

    def _verify_signin(self, token: str = None):
        env: Mapping
        account = None
        # copy os.environ to a dict since its type is incompatible
        # with Dict[str, str], as reported by mypy
        env = dict(environ)
        if token and self._sess_var:
            # we need to pass an environment dictionary to subprocess.run() that contains
            # the session token we're trying to verify
            #
            # Above we made a copy of os.environ, so we're not modifying it at this point
            # we'll offically set it once we know it works
            env[self._sess_var] = token

        # this step actually talks to the 1Password account
        # it uses "op whoami" which is a very non-intrusive
        # query that will fail without authentication
        try:
            account = self._whoami(self.op_path, env=env)
        except OPWhoAmiException as ocfe:
            # scrape error message about not being signed in

            fragments = [self.NO_ACTIVE_SESSION_FOUND_TEXT,
                         self.NOT_SIGNED_IN_TEXT,
                         self.NO_SESSION_TOKEN_FOUND_TEXT,
                         self.ACCT_IS_NOT_SIGNED_IN_TEXT]
            unknown_err = True
            for frag in fragments:
                if frag in ocfe.err_output:
                    unknown_err = False
                    break
            # there was a different error so raise the exception
            if unknown_err:  # pragma: no cover
                raise ocfe

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
            raise OPAuthenticationException(
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
                               input=password, decode="utf-8")
        except OPCmdFailedException as ocfe:
            raise OPSigninException.from_opexception(ocfe) from ocfe

        return output

    @classmethod
    def _run_with_auth_check(cls,
                             op_path: str,
                             account: str,
                             argv: _OPArgv,
                             capture_stdout: bool = False,
                             input: Union[str, bytes] = None,
                             decode: str = None,
                             env: Mapping = environ):
        # this somewhat of a hack to detect if authentication has expired
        # so that we can raise OPAuthenticationException rather than the generic OPCmdFailedException
        # under the hood, it calls 'whoami' which will fail if not authenticated
        #
        # We need to remove this as soon as possible if a better way becomes available
        # among the problems:
        # - this method is racey, since authentication may expire between the check and the
        #   operation
        # - this adds roughly 20% overhead (as measured by the full suite of pytest tests)
        if cls._auth_expired(op_path, account):
            raise OPAuthenticationException(
                "Authentication has expired")  # pragma: no cover

        if cls.svc_account_env_var_set():
            err_msg = None
            supported = argv.svc_account_supported()
            if supported.code in [SVC_ACCT_INCOMPAT_OPTIONS, SVC_ACCT_CMD_NOT_SUPPORTED]:
                err_msg = supported.msg
            elif supported.code == SVC_ACCT_SUPPORTED:
                cls.logger.debug("Command supported with service accounts")
            else:
                raise Exception(  # pragma: no cover
                    f"Unknown service account support code {supported.code}")

            if err_msg:
                if cls._should_log_op_errors():
                    cls.logger.error(err_msg)
                raise OPSvcAcctCommandNotSupportedException(err_msg)

        return cls._run(argv,
                        capture_stdout=capture_stdout,
                        input=input,
                        decode=decode,
                        env=env)

    @classmethod
    def _item_template_list_special(cls, op_path,  env: Dict[str, str] = None):
        if not env:
            env = dict(environ)
        # special "template list" class method we can use for testing authentication
        argv = _OPArgv.item_template_list_argv(op_path)
        template_list_json = cls._run(
            argv, capture_stdout=True, decode="utf-8", env=env)
        return template_list_json

    @classmethod
    def _whoami_base(cls, op_path, env: Dict[str, str] = None, account: str = None):
        if not env:
            env = dict(environ)
        argv = _OPArgv.whoami_argv(op_path, account=account)
        account_json = cls._run(
            argv, capture_stdout=True, decode="utf-8", env=env)
        return account_json

    @classmethod
    def _whoami_svc_account(cls, op_path, env: Dict[str, str] = None):
        # whoami behaves differently under certain circumstances if OP_SERVICE_ACCOUNT_TOKEN
        # is set, and we need to handle this situations differently
        # They include:
        # - service account env variable is set, but token is malformed
        # - on op >= 2.20.0, service account token is set, but not yet "authenticated"
        account_json = None
        attempts = 0
        max_attempts = 2
        while account_json is None:
            # try once, and if necessary try "item template list" to authenticate
            # then try at most one more time
            attempts += 1
            try:
                account_json = cls._whoami_base(op_path, env=env)
            except OPCmdFailedException as ocfe:
                if attempts < max_attempts and cls.SVC_ACCT_TOKEN_NOT_AUTH_TXT in ocfe.err_output:
                    # Trigger a service account authenticated session (v 2.20.0 and later)
                    cls._item_template_list_special(op_path, env=env)
                    continue
                elif cls.SVC_ACCT_TOKEN_MALFORMED_TEXT in ocfe.err_output:  # pragma: no cover
                    # OP_SERVICE_ACCOUNT_TOKEN got set to something malformed
                    # so raise a specific exception for that
                    raise OPCmdMalformedSvcAcctTokenException.from_opexception(
                        ocfe)
                    # Although we could simulate this for testing, the tests
                    # wouldn't be meaningful, because they wouldn't be tied to
                    # an actual malformed token
                    # disabling testing coverage
                else:
                    raise  # pragma: no cover

        return account_json

    @classmethod
    def _whoami(cls, op_path, env: Dict[str, str] = None, account: str = None) -> OPAccount:
        # outer/normal whoami method
        # if a service account var is set, this method will call
        # _whoami_svc_account(), which will call _whoami_base()
        # otherwise, this method calls _whoami_base()

        try:
            if cls.svc_account_env_var_set():
                account_json = cls._whoami_svc_account(op_path, env=env)
            else:
                account_json = cls._whoami_base(
                    op_path, env=env, account=account)
        except OPCmdFailedException as ocfe:
            raise OPWhoAmiException.from_opexception(ocfe)

        account_obj = OPAccount(account_json)
        return account_obj

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
            document_bytes = self._run_with_auth_check(
                self.op_path, self._account_identifier, get_document_argv, capture_stdout=True)
        except OPCmdFailedException as ocfe:
            raise OPDocumentGetException.from_opexception(ocfe) from ocfe

        if self._cli_version <= DOCUMENT_BYTES_BUG_VERSION:  # pragma: no cover
            # op versions 2.0.0 - 2.2.0 append an erroneous \x0a ('\n') byte to document bytes
            # trim it off if its present
            if document_bytes[-1] == 0x0a:
                document_bytes = document_bytes[:-1]
            else:
                # this shouldn't happen but maybe an edge case?
                pass

        return document_bytes

    def _document_edit(self,
                       document_identifier: str,
                       document_bytes: bytes,
                       file_name: Optional[str] = None,
                       new_title: Optional[str] = None,
                       vault: Optional[str] = None):

        document_edit_argv = self._document_edit_argv(
            document_identifier, file_name=file_name, new_title=new_title, vault=vault)
        try:
            # 'op document edit' doesn't have any output if successful
            # if it fails, stderr will be in the exception object
            self._run_with_auth_check(
                self.op_path, self._account_identifier, document_edit_argv, input=document_bytes)
        except OPCmdFailedException as ocfe:
            raise OPDocumentEditException.from_opexception(ocfe)

        return

    def _document_delete(self, document_name_or_id: str, vault: Optional[str] = None, archive=False):

        document_delete_argv = self._document_delete_argv(
            document_name_or_id, vault=vault, archive=archive)
        try:
            # 'op document delete' doesn't have any output if successful
            # if it fails, stderr will be in the exception object
            self._run_with_auth_check(
                self.op_path, self._account_identifier, document_delete_argv)
        except OPCmdFailedException as ocfe:
            raise OPDocumentDeleteException.from_opexception(ocfe)

        return

    def _item_get(self, item_name_or_id, vault=None, fields=None, include_archive=False, decode="utf-8"):
        item_get_argv = self._item_get_argv(
            item_name_or_id, vault=vault, fields=fields, include_archive=include_archive)
        try:
            output = self._run_with_auth_check(
                self.op_path, self._account_identifier, item_get_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPItemGetException.from_opexception(ocfe) from ocfe

        return output

    def _item_delete(self, item_name_or_id, vault=None, archive=False, decode="utf-8"):
        item_delete_argv = self._item_delete_argv(
            item_name_or_id, vault=vault, archive=archive)
        try:
            # 'op item delete' doesn't have any output if successful
            # if it fails, stderr will be in the exception object
            self._run_with_auth_check(
                self.op_path, self._account_identifier, item_delete_argv, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPItemDeleteException.from_opexception(ocfe)

        return

    def _item_delete_multiple(self, batch_json, vault, archive=False):
        # op item delete takes '-' for the item to delete if objects are
        # provided over stdin
        item_id = "-"
        item_delete_argv = self._item_delete_argv(
            item_id, vault=vault, archive=archive)
        try:
            # 'op item delete' doesn't have any output if successful
            # if it fails, stderr will be in the exception object
            self._run_with_auth_check(
                self.op_path, self._account_identifier, item_delete_argv, input=batch_json)
        except OPCmdFailedException as ocfe:
            # OPItemDeleteException will get turned into
            # OPItemDeleteMultipleException by the caller, so
            # any sucessfully deleted items can be included in the exception object
            raise OPItemDeleteException.from_opexception(ocfe)

        return

    def _item_get_totp(self, item_name_or_id, vault=None, decode="utf-8"):
        item_get_totp_argv = self._item_get_totp_argv(
            item_name_or_id, vault=vault)
        try:
            output = self._run_with_auth_check(self.op_path, self._account_identifier,
                                               item_get_totp_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPItemGetException.from_opexception(ocfe) from ocfe

        return output

    @classmethod
    def _signed_in_accounts(cls, op_path, decode="utf-8"):
        account_list_argv = cls._account_list_argv(op_path, encoding=decode)
        output = cls._run(account_list_argv,
                          capture_stdout=True, decode=decode)
        return output

    def _user_get(self, user_name_or_id: str, decode: str = "utf-8") -> str:
        user_get_argv = self._user_get_argv(user_name_or_id)
        try:
            output = self._run_with_auth_check(self.op_path, self._account_identifier,
                                               user_get_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPUserGetException.from_opexception(ocfe) from ocfe
        return output

    def _user_edit(self,
                   user_name_or_id: str,
                   new_name: Optional[str],
                   travel_mode: Optional[bool],
                   decode: str = "utf-8"):

        user_edit_argv = self._user_edit_argv(
            user_name_or_id, new_name, travel_mode)

        try:
            # 'op user edit' doesn't have any output if successful
            # if it fails, stderr will be in the exception object
            self._run_with_auth_check(self.op_path, self._account_identifier,
                                      user_edit_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPUserEditException.from_opexception(ocfe) from ocfe
        return

    def _user_list(self, group_name_or_id=None, vault=None, decode: str = "utf-8") -> str:
        user_list_argv = self._user_list_argv(
            group_name_or_id=group_name_or_id, vault=vault)
        try:
            output = self._run_with_auth_check(self.op_path, self._account_identifier,
                                               user_list_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPUserListException.from_opexception(ocfe)
        return output

    def _group_get(self, group_name_or_id: str, decode: str = "utf-8") -> str:
        group_get_argv = self._group_get_argv(group_name_or_id)
        try:
            output = self._run_with_auth_check(self.op_path, self._account_identifier,
                                               group_get_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPGroupGetException.from_opexception(ocfe) from ocfe
        return output

    def _group_list(self, user_name_or_id=None, vault=None, decode: str = "utf-8") -> str:
        group_list_argv = self._group_list_argv(
            user_name_or_id=user_name_or_id, vault=vault)
        try:
            output = self._run_with_auth_check(self.op_path, self._account_identifier,
                                               group_list_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPGroupListException.from_opexception(ocfe)
        return output

    def _vault_get(self, vault_name_or_id: str, decode: str = "utf-8") -> str:
        vault_get_argv = self._vault_get_argv(vault_name_or_id)
        try:
            output = self._run_with_auth_check(self.op_path, self._account_identifier,
                                               vault_get_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPVaultGetException.from_opexception(ocfe)
        return output

    def _vault_list(self, group_name_or_id=None, user_name_or_id=None, decode="utf-8") -> str:
        vault_list_argv = self._vault_list_argv(
            group_name_or_id=group_name_or_id, user_name_or_id=user_name_or_id)
        try:
            output = self._run_with_auth_check(self.op_path, self._account_identifier,
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
    def _account_forget(cls, account: str, op_path=None):   # pragma: no cover
        if not op_path:
            op_path = cls.OP_PATH
        argv = _OPArgv.account_forget_argv(op_path, account)
        cls._run(argv)

    def _item_list(self, categories=[], include_archive=False, tags=[], vault=None, decode="utf-8"):
        # default lists to the categories & list kwargs
        # get initialized at module load
        # so its the same list object on every call to this funciton
        # This really isn't what we want, so the easiest
        # mitigation is to just make a copy of whatever list was passed in
        # or of the default kwarg if nothing was passed in
        categories = list(categories)
        tags = list(tags)
        argv = self._item_list_argv(
            categories=categories, include_archive=include_archive, tags=tags, vault=vault)
        try:
            output = self._run_with_auth_check(
                self.op_path, self._account_identifier, argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as e:
            raise OPItemListException.from_opexception(e)
        return output

    def _item_create(self, item, vault, password_recipe, decode="utf-8"):
        argv = self._item_create_argv(item, password_recipe, vault)
        try:
            output = self._run_with_auth_check(
                self.op_path, self._account_identifier, argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as e:
            raise OPItemCreateException.from_opexception(e)

        return output

    def _item_edit_run(self, argv: _OPArgv, decode: str):
        try:
            output = self._run_with_auth_check(
                self.op_path, self._account_identifier, argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as e:
            raise OPItemEditException.from_opexception(e)

        return output

    def _item_edit_set_field_value(self,
                                   item_identifier: str,
                                   field_type: OPFieldTypeEnum,
                                   value: str,
                                   field_label: str,
                                   section_label: Optional[str] = None,
                                   vault: Optional[str] = None,
                                   decode: str = "utf-8") -> str:
        argv = self._item_edit_set_field_value_argv(item_identifier,
                                                    field_type,
                                                    value,
                                                    field_label=field_label,
                                                    section_label=section_label,
                                                    vault=vault)
        output = self._item_edit_run(argv, decode)
        return output

    def _item_edit_favorite(self,
                            item_identifier: str,
                            favorite: bool,
                            vault: Optional[str] = None,
                            decode: str = "utf-8"):
        argv = self._item_edit_favorite_argv(
            item_identifier, favorite, vault=vault)

        output = self._item_edit_run(argv, decode)
        return output

    def _item_edit_generate_password(self,
                                     item_identifier: str,
                                     password_recipe: OPPasswordRecipe,
                                     vault=None,
                                     decode="utf-8") -> str:
        argv = self._item_edit_generate_password_argv(
            item_identifier, password_recipe, vault)

        output = self._item_edit_run(argv, decode)
        return output

    def _item_edit_tags(self,
                        item_identifier: str,
                        tags: List[str],
                        vault: Optional[str] = None,
                        decode: str = "utf-8"):
        argv = self._item_edit_tags_argv(
            item_identifier, tags, vault=vault)

        output = self._item_edit_run(argv, decode)
        return output

    def _item_edit_title(self,
                         item_identifier: str,
                         item_title: str,
                         vault: Optional[str] = None,
                         decode: str = "utf-8"):
        argv = self._item_edit_title_argv(
            item_identifier, item_title, vault=vault)

        output = self._item_edit_run(argv, decode)
        return output

    def _item_edit_url(self,
                       item_identifier: str,
                       url: str,
                       vault: Optional[str] = None,
                       decode: str = "utf-8"):
        argv = self._item_edit_url_argv(
            item_identifier, url, vault=vault)

        output = self._item_edit_run(argv, decode)
        return output

    @classmethod
    def _account_list_argv(cls, op_path="op", encoding="utf-8"):
        argv = _OPArgv.account_list_argv(op_path, encoding=encoding)
        return argv

    def _document_get_argv(self,
                           document_name_or_id: str,
                           vault: Optional[str] = None,
                           include_archive: Optional[bool] = False):
        vault_arg = vault if vault else self.vault
        document_get_argv = _OPArgv.document_get_argv(self.op_path,
                                                      document_name_or_id,
                                                      vault=vault_arg,
                                                      include_archive=include_archive)

        return document_get_argv

    def _document_edit_argv(self,
                            document_identifier: str,
                            file_name: Optional[str] = None,
                            new_title: Optional[str] = None,
                            vault: Optional[str] = None):
        vault_arg = vault if vault else self.vault
        document_edit_argv = _OPArgv.document_edit_argv(self.op_path,
                                                        document_identifier,
                                                        file_name=file_name,
                                                        new_title=new_title,
                                                        vault=vault_arg)

        return document_edit_argv

    def _document_delete_argv(self, document_name_or_id: str, vault: Optional[str] = None, archive=False):
        vault_arg = vault if vault else self.vault

        document_delete_argv = _OPArgv.document_delete_argv(
            self.op_path, document_name_or_id, vault=vault_arg, archive=archive)

        return document_delete_argv

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

    def _user_get_argv(self, user_name_or_id: str):
        get_user_argv = _OPArgv.user_get_argv(self.op_path, user_name_or_id)
        return get_user_argv

    def _user_edit_argv(self, user_name_or_id: str, new_name: Optional[str], travel_mode: Optional[bool]):
        get_user_argv = _OPArgv.user_edit_argv(self.op_path,
                                               user_name_or_id,
                                               new_name,
                                               travel_mode)
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

    def _item_create_argv(self, item, password_recipe, vault):
        vault_arg = vault if vault else self.vault
        item_create_argv = _OPArgv.item_create_argv(
            self.op_path, item, password_recipe=password_recipe, vault=vault_arg
        )
        return item_create_argv

    def _item_edit_set_field_value_argv(self,
                                        item_identifier: str,
                                        field_type: OPFieldTypeEnum,
                                        value: str,
                                        field_label: str,
                                        section_label: Optional[str],
                                        vault: Optional[str]):
        vault_arg = vault if vault else self.vault
        item_edit_argv = _OPArgv.item_edit_set_field_value(self.op_path,
                                                           item_identifier,
                                                           field_type,
                                                           value,
                                                           field_label=field_label,
                                                           section_label=section_label,
                                                           vault=vault_arg)
        return item_edit_argv

    def _item_edit_favorite_argv(self,
                                 item_identifier: str,
                                 favorite: bool,
                                 vault: Optional[str]):
        vault_arg = vault if vault else self.vault

        item_edit_argv = _OPArgv.item_edit_favorite(self.op_path,
                                                    item_identifier,
                                                    favorite,
                                                    vault=vault_arg)
        return item_edit_argv

    def _item_edit_generate_password_argv(self,
                                          item_identifier: str,
                                          password_recipe: OPPasswordRecipe,
                                          vault: Optional[str]):

        vault_arg = vault if vault else self.vault
        item_edit_argv = _OPArgv.item_edit_generate_password_argv(self.op_path,
                                                                  item_identifier,
                                                                  password_recipe,
                                                                  vault=vault_arg)
        return item_edit_argv

    def _item_edit_tags_argv(self,
                             item_identifier: str,
                             tags: List[str],
                             vault: Optional[str]):
        vault_arg = vault if vault else self.vault

        item_edit_argv = _OPArgv.item_edit_tags(self.op_path,
                                                item_identifier,
                                                tags,
                                                vault=vault_arg)

        return item_edit_argv

    def _item_edit_title_argv(self,
                              item_identifier: str,
                              item_title: str,
                              vault: Optional[str]):
        vault_arg = vault if vault else self.vault

        item_edit_argv = _OPArgv.item_edit_title(self.op_path,
                                                 item_identifier,
                                                 item_title,
                                                 vault=vault_arg)
        return item_edit_argv

    def _item_edit_url_argv(self,
                            item_identifier: str,
                            url: str,
                            vault: Optional[str]):
        vault_arg = vault if vault else self.vault

        item_edit_argv = _OPArgv.item_edit_url(self.op_path,
                                               item_identifier,
                                               url,
                                               vault=vault_arg)
        return item_edit_argv

    def _item_list_argv(self, categories=[], include_archive=False, tags=[], vault=None):
        # default lists to the categories & list kwargs
        # get initialized at module load
        # so its the same list object on every call to this funciton
        # This really isn't what we want, so the easiest
        # mitigation is to just make a copy of whatever list was passed in
        # or of the default kwarg if nothing was passed in
        categories = list(categories)
        tags = list(tags)
        vault_arg = vault if vault else self.vault
        list_items_argv = _OPArgv.item_list_argv(self.op_path,
                                                 categories=categories, include_archive=include_archive, tags=tags, vault=vault_arg)
        return list_items_argv
