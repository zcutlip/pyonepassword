import json
import os
import pathlib
from json.decoder import JSONDecodeError
from typing import List, Optional

from .py_op_exceptions import OPConfigNotFoundException


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
        self._configpath = configpath
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

        accounts = self._initialize_account_objects()
        self["accounts"] = accounts

        account_map = {}
        for account in accounts:
            account_map[account.shorthand] = account
        self.account_map = account_map

    def _get_config_path(self) -> pathlib.Path:
        configpath: pathlib.Path = None
        config_home = None
        try:
            config_home = pathlib.Path(os.environ['XDG_CONFIG_HOME'])

        except KeyError:
            config_home = pathlib.Path.home()

        for subpath in self.OP_CONFIG_PATHS:
            _configpath = pathlib.Path(config_home, subpath)
            if os.path.exists(_configpath):
                configpath = _configpath
                break

        return configpath

    def _initialize_account_objects(self) -> List[OPCLIAccountConfig]:
        account_list = self.accounts
        account_objects = []
        acct: OPCLIAccountConfig
        for account_dict in account_list:
            acct = OPCLIAccountConfig(account_dict)
            account_objects.append(acct)

        return account_objects

    @property
    def accounts(self) -> List[OPCLIAccountConfig]:
        account_list = self.get("accounts")
        if account_list is None:
            account_list = []
        return account_list

    @property
    def latest_signin(self) -> Optional[str]:
        return self.get("latest_signin")

    @property
    def latest_signin_uuid(self) -> Optional[str]:
        latest_uuid = None
        latest = self.latest_signin
        if latest:
            latest_uuid = self.uuid_for_account(latest)
        return latest_uuid

    def get_config(self, account_id=None) -> OPCLIAccountConfig:
        if account_id is None:
            account_id = self.get("latest_signin")
        if not account_id:  # if shorthand is None or empty string
            raise OPConfigNotFoundException(
                "No account identifier provided, no sign-ins found.")

        config = self.account_map.get(account_id)
        if not config:
            for account in self.accounts:
                if account_id in [account.account_uuid, account.user_uuid, account.shorthand, account.email, account.url]:
                    config = account
                    break

        if config is None:
            raise OPConfigNotFoundException(
                f"No config found for account identifier '{account_id}'")
        return config

    def uuid_for_account(self, account_identifier) -> str:
        config = self.get_config(account_id=account_identifier)
        uuid = config.user_uuid
        return uuid
