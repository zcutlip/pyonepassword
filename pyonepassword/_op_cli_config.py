import json
import os
import pathlib
from json.decoder import JSONDecodeError
from typing import Dict, List

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
