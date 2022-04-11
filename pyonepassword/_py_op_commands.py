"""
Description: A module that maps methods to to `op` commands and subcommands
"""
import json
import os
import pathlib
from json.decoder import JSONDecodeError
from os import environ as env
from typing import List

from ._py_op_cli import _OPArgv, _OPCLIExecute
from .op_cli_version import MINIMUM_ITEM_CREATION_VERSION, OPCLIVersion
from .op_items._op_items_base import OPAbstractItem
from .py_op_exceptions import (
    OPCmdFailedException,
    OPConfigNotFoundException,
    OPCreateItemException,
    OPCreateItemNotSupportedException,
    OPGetGroupException,
    OPGetItemException,
    OPGetDocumentException,
    OPGetUserException,
    OPGetVaultException,
    OPNotSignedInException,
)


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

    def get_config(self, shorthand=None):
        if shorthand is None:
            shorthand = self.get("latest_signin")
        if shorthand is None:
            raise OPConfigNotFoundException(
                "No shorthand provided, no sign-ins found.")
        accounts: List = self["accounts"]
        config = None
        for acct in accounts:
            if acct["shorthand"] == shorthand:
                config = acct

        if config is None:
            raise OPConfigNotFoundException(
                f"No config found for shorthand {shorthand}")

        return config


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
        if logger:
            self.logger = logger
        self._token = None
        self.op_path = op_path

        self._cli_version: OPCLIVersion = self._get_cli_version(op_path)

        uses_bio = self.uses_biometric(
            self.op_path, account_shorthand=account_shorthand)

        if account_shorthand is None and not uses_bio:
            account_shorthand = self._get_account_shorthand()
        self.account_shorthand = account_shorthand

        if self.account_shorthand is None and not uses_bio:
            raise OPNotSignedInException(
                "Account shorthand not provided and not found in 'op' config")

        sess_var_name = 'OP_SESSION_{}'.format(account_shorthand)
        if use_existing_session:
            self._token = self._verify_signin(sess_var_name)

        if not self._token:
            if not password and not password_prompt and not uses_bio:
                # we don't have a token, weren't provided a password
                # and were told not to let 'op' prompt for a password
                raise OPNotSignedInException(
                    "No existing session and no password provided.")
            # We don't have a token but eitehr are have a password
            # or op should be allowed to prompt for one
            self._token = self._do_normal_signin(account_shorthand, password)

        self._sess_var = sess_var_name
        # export OP_SESSION_<signin_address>
        env[sess_var_name] = self.token

    def supports_item_creation(self):
        support = False
        if self._cli_version >= MINIMUM_ITEM_CREATION_VERSION:
            support = True
        return support

    def _get_item_argv(self, item_name_or_uuid, vault=None, fields=None):
        vault_arg = vault if vault else self.vault

        lookup_argv = _OPArgv.get_item_argv(
            self.op_path, item_name_or_uuid, vault=vault_arg, fields=fields)
        return lookup_argv

    def _get_totp_argv(self, item_name_or_uuid, vault=None):
        vault_arg = vault if vault else self.vault

        lookup_argv = _OPArgv.get_totp_argv(
            self.op_path, item_name_or_uuid, vault=vault_arg)
        return lookup_argv

    def _get_document_argv(self, document_name_or_uuid: str, vault: str = None):
        vault_arg = vault if vault else self.vault

        get_document_argv = _OPArgv.get_document_argv(
            self.op_path, document_name_or_uuid, vault=vault_arg)

        return get_document_argv

    def _get_user_argv(self, user_name_or_uuid: str):
        get_user_argv = _OPArgv.get_generic_argv(
            self.op_path, "user", user_name_or_uuid, [])
        return get_user_argv

    def _get_group_argv(self, group_name_or_uuid: str):
        get_group_argv = _OPArgv.get_generic_argv(
            self.op_path, "group", group_name_or_uuid, [])
        return get_group_argv

    def _get_vault_argv(self, vault_name_or_uuid: str):
        get_vault_argv = _OPArgv.get_generic_argv(
            self.op_path, "vault", vault_name_or_uuid, [])
        return get_vault_argv

    def _cli_version_argv(self):
        # Specifically for use by mock_op response-generator
        cli_version_argv = _OPArgv.cli_version_argv(self.op_path)
        return cli_version_argv

    def _get_item(self, item_name_or_uuid, vault=None, fields=None, decode="utf-8"):
        get_item_argv = self._get_item_argv(
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

    def _get_document(self, document_name_or_uuid: str, vault: str = None):
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

    def _get_user(self, user_name_or_uuid: str, decode: str = "utf-8") -> str:
        get_user_argv = self._get_user_argv(user_name_or_uuid)
        try:
            output = self._run(
                get_user_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPGetUserException.from_opexception(ocfe) from ocfe
        return output

    def _get_group(self, group_name_or_uuid: str, decode: str = "utf-8") -> str:
        get_group_argv = self._get_group_argv(group_name_or_uuid)
        try:
            output = self._run(
                get_group_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPGetGroupException.from_opexception(ocfe) from ocfe
        return output

    def _get_vault(self, vault_name_or_uuid: str, decode: str = "utf-8") -> str:
        get_vault_argv = self._get_vault_argv(vault_name_or_uuid)
        try:
            output = self._run(
                get_vault_argv, capture_stdout=True, decode=decode
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
        argv = _OPArgv.signout_argv(
            self.op_path, account, session, forget=forget)
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
