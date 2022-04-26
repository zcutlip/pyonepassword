"""
Description: A module that maps methods to to `op` commands and subcommands
"""
import json
import logging
import os
import pathlib
from json.decoder import JSONDecodeError
from os import environ as env
from typing import Dict, List

from ._py_op_cli import _OPArgv, _OPCLIExecute
from .account import OPAccount, OPAccountList
from .op_cli_version import MINIMUM_ITEM_CREATION_VERSION, OPCLIVersion
from .op_items._op_items_base import OPAbstractItem
from .py_op_exceptions import (
    OPCmdFailedException,
    OPConfigNotFoundException,
    OPCreateItemException,
    OPCreateItemNotSupportedException,
    OPGetDocumentException,
    OPGetGroupException,
    OPGetItemException,
    OPGetUserException,
    OPGetVaultException,
    OPNotSignedInException,
    OPSigninException
)


class OPCLIAccountConfig(dict):

    def __init__(self, account_dict):
        super().__init__(account_dict)

    @property
    def shorthand(self) -> str:
        return self["shorthand"]

    @property
    def account_uuid(self) -> str:
        return self["accountUUID"]

    @property
    def url(self) -> str:
        return self["url"]

    @property
    def email(self) -> str:
        return self["email"]

    @property
    def account_key(self) -> str:
        return self["accountKey"]

    @property
    def user_uuid(self) -> str:
        return self["userUUID"]


class OPCLIConfig(dict):
    OP_CONFIG_PATHS = [
        pathlib.Path(".config", "op", "config"),
        pathlib.Path(".op", "config")
    ]

    def __init__(self, configpath=None):
        super().__init__()
        if configpath is None:
            configpath = self._get_config_path()
        self.configpath = configpath
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

        self.account_map = self._initialize_account_objects()

    def _get_config_path(self):
        configpath = None
        config_home = None
        try:
            config_home = os.environ['XDG_CONFIG_HOME']
        except KeyError:
            config_home = pathlib.Path.home()

        for subpath in self.OP_CONFIG_PATHS:
            _configpath = pathlib.Path(config_home, subpath)
            if os.path.exists(_configpath):
                configpath = _configpath
                break

        return configpath

    def _initialize_account_objects(self):
        account_list = self.accounts
        account_objects = []
        account_map = {}
        acct: OPCLIAccountConfig
        for account_dict in account_list:
            acct = OPCLIAccountConfig(account_dict)
            account_objects.append(acct)
            account_map[acct.shorthand] = acct
        return account_map

    @property
    def accounts(self) -> List[Dict[str, str]]:
        return self["accounts"]

    def get_config(self, shorthand=None) -> OPCLIAccountConfig:
        if shorthand is None:
            shorthand = self.get("latest_signin")
        if shorthand is None:
            raise OPConfigNotFoundException(
                "No shorthand provided, no sign-ins found.")

        try:
            config = self.account_map[shorthand]
        except KeyError:
            raise OPConfigNotFoundException(
                f"No config found for shorthand {shorthand}")

        return config

    def uuid_for_shorthand(self, shorthand) -> str:
        config = self.get_config(shorthand=shorthand)
        uuid = config.user_uuid
        return uuid


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
                 use_existing_session=False,
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
        self._token = None
        self.op_path = op_path

        self._cli_version: OPCLIVersion = self._get_cli_version(op_path)

        self.uses_bio = self.uses_biometric(
            self.op_path, account_shorthand=account_shorthand)
        op_config = OPCLIConfig()
        if account_shorthand is None and not self.uses_bio:
            account_shorthand = self._get_account_shorthand(op_config)
            if account_shorthand is None:
                raise OPNotSignedInException(
                    "Account shorthand not provided and not found in 'op' config")

        self.account_shorthand = account_shorthand

        sess_var_name = None

        if account_shorthand and not self.uses_bio:
            user_uuid = op_config.uuid_for_shorthand(account_shorthand)
            sess_var_name = 'OP_SESSION_{}'.format(user_uuid)

        if use_existing_session and sess_var_name:
            self._token = self._verify_signin(sess_var_name)

        if not self._token:
            if not password and not password_prompt and not self.uses_bio:
                # we don't have a token, weren't provided a password
                # and were told not to let 'op' prompt for a password
                raise OPNotSignedInException(
                    "No existing session and no password provided.")
            # We don't have a token but eitehr are have a password
            # or op should be allowed to prompt for one
            self._token = self._do_normal_signin(account_shorthand, password)

        self._sess_var = sess_var_name
        # export OP_SESSION_<signin_address>
        if sess_var_name and self.token:
            env[sess_var_name] = self.token

    @property
    def token(self) -> str:
        return self._token

    @property
    def session_var(self) -> str:
        return self._sess_var

    def _get_account_shorthand(self, config):
        try:
            account_shorthand = config['latest_signin']
            self.logger.debug(
                "Using account shorthand found in op config: {}".format(account_shorthand))
        except KeyError:
            account_shorthand = None
        return account_shorthand

    def _get_cli_version(self, op_path):
        argv = _OPArgv.cli_version_argv(op_path)
        output = self._run(argv, capture_stdout=True, decode="utf-8")
        output = output.rstrip()
        cli_version = OPCLIVersion(output)
        return cli_version

    def _verify_signin(self, sess_var_name):
        # Need to get existing token if we're already signed in
        token = env.get(sess_var_name)

        if token:
            # if there's no token, no need to sign in
            argv = _OPArgv.get_verify_signin_argv(self.op_path)
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
        signin_argv = _OPArgv.normal_signin_argv(
            self.op_path, account_shorthand=account_shorthand)

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
    def uses_biometric(cls, op_path="op", account_shorthand=None, encoding="utf-8"):
        uses_bio = True
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

    def supports_item_creation(self):
        support = False
        if self._cli_version >= MINIMUM_ITEM_CREATION_VERSION:
            support = True
        return support

    @classmethod
    def _account_list_argv(cls, op_path="op", encoding="utf-8"):
        argv = _OPArgv.account_list_argv(op_path, encoding=encoding)
        return argv

    def _item_get_argv(self, item_name_or_uuid, vault=None, fields=None):
        vault_arg = vault if vault else self.vault

        lookup_argv = _OPArgv.item_get_argv(
            self.op_path, item_name_or_uuid, vault=vault_arg, fields=fields)
        return lookup_argv

    def _get_totp_argv(self, item_name_or_uuid, vault=None):
        vault_arg = vault if vault else self.vault

        lookup_argv = _OPArgv.get_totp_argv(
            self.op_path, item_name_or_uuid, vault=vault_arg)
        return lookup_argv

    def _get_document_argv(self, document_name_or_uuid: str, vault: str = None):
        vault_arg = vault if vault else self.vault

        get_document_argv = _OPArgv.document_get_argv(
            self.op_path, document_name_or_uuid, vault=vault_arg)

        return get_document_argv

    def _user_get_argv(self, user_name_or_uuid: str):
        get_user_argv = _OPArgv.user_get_argv(self.op_path, user_name_or_uuid)
        return get_user_argv

    def _group_get_argv(self, group_name_or_uuid: str):
        group_get_argv = _OPArgv.group_get_argv(
            self.op_path, group_name_or_uuid)
        return group_get_argv

    def _vault_get_argv(self, vault_name_or_uuid: str):

        get_vault_argv = _OPArgv.vault_get_argv(
            self.op_path, vault_name_or_uuid)
        return get_vault_argv

    def _cli_version_argv(self):
        # Specifically for use by mock_op response-generator
        cli_version_argv = _OPArgv.cli_version_argv(self.op_path)
        return cli_version_argv

    def _item_get(self, item_name_or_uuid, vault=None, fields=None, decode="utf-8"):
        get_item_argv = self._item_get_argv(
            item_name_or_uuid, vault=vault, fields=fields)
        try:
            output = self._run(
                get_item_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPGetItemException.from_opexception(ocfe) from ocfe

        return output

    def _get_totp(self, item_name_or_uuid, vault=None, decode="utf-8"):
        get_totp_argv = self._get_totp_argv(
            item_name_or_uuid, vault=vault)
        try:
            output = self._run(
                get_totp_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPGetItemException.from_opexception(ocfe) from ocfe

        return output

    def _document_get(self, document_name_or_uuid: str, vault: str = None):
        """
        Download a document object from a 1Password vault by name or UUID.

        Arguments:
            - 'item_name_or_uuid': The item to look up
        Raises:
            - OPGetDocumentException if the lookup fails for any reason.
            - OPNotFoundException if the 1Password command can't be found.
        Returns:
            - Bytes: document bytes
        """

        get_document_argv = self._get_document_argv(
            document_name_or_uuid, vault=vault)

        try:
            document_bytes = self._run(get_document_argv, capture_stdout=True)
        except OPCmdFailedException as ocfe:
            raise OPGetDocumentException.from_opexception(ocfe) from ocfe

        return document_bytes

    def _user_get(self, user_name_or_uuid: str, decode: str = "utf-8") -> str:
        get_user_argv = self._user_get_argv(user_name_or_uuid)
        try:
            output = self._run(
                get_user_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPGetUserException.from_opexception(ocfe) from ocfe
        return output

    def _get_group(self, group_name_or_uuid: str, decode: str = "utf-8") -> str:
        get_group_argv = self._group_get_argv(group_name_or_uuid)
        try:
            output = self._run(
                get_group_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPGetGroupException.from_opexception(ocfe) from ocfe
        return output

    def _vault_get(self, vault_name_or_uuid: str, decode: str = "utf-8") -> str:
        vault_get_argv = self._vault_get_argv(vault_name_or_uuid)
        try:
            output = self._run(
                vault_get_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPGetVaultException.from_opexception(ocfe)
        return output

    def _create_item(self, item: OPAbstractItem, item_name, vault=None):
        if not self.supports_item_creation():
            msg = f"Minimum supported 'op' version for item creation: {MINIMUM_ITEM_CREATION_VERSION}, current version: {self._cli_version}"
            raise OPCreateItemNotSupportedException(msg)
        argv = self._create_item_argv(item, item_name, vault)
        try:
            output = self._run(
                argv, capture_stdout=True, decode="utf-8"
            )
        except OPCmdFailedException as ocfe:
            raise OPCreateItemException.from_opexception(ocfe)

        return output

    def _signout(self, account, session, forget=False):
        if forget and self.uses_bio:
            self.logger.warn(
                "Biometric is enabled. 'forget' operation will have no effect.")
        argv = _OPArgv.signout_argv(
            self.op_path, account, session, forget=forget, uses_bio=self.uses_bio)
        self._run(argv)

    @classmethod
    def _forget(cls, account: str, op_path=None):
        if not op_path:
            op_path = cls.OP_PATH
        argv = _OPArgv.forget_argv(op_path, account)
        cls._run(argv)

    def _create_item_argv(self, item, item_name, vault):
        vault_arg = vault if vault else self.vault
        create_item_argv = _OPArgv.create_item_argv(
            self.op_path, item, item_name, vault=vault_arg
        )
        return create_item_argv

    def _list_items_argv(self, categories=[], include_archive=False, tags=[], vault=None):
        vault_arg = vault if vault else self.vault
        list_items_argv = _OPArgv.list_items_argv(self.op_path,
                                                  categories=categories, include_archive=include_archive, tags=tags, vault=vault_arg
                                                  )
        return list_items_argv

    def _list_items(self, categories=[], include_archive=False, tags=[], vault=None, decode="utf-8"):
        argv = self._list_items_argv(
            categories=categories, include_archive=include_archive, tags=tags, vault=vault)
        try:
            output = self._run(argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as e:
            raise e
        return output
