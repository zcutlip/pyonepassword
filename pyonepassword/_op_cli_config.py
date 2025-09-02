import json
import logging
import os
from json.decoder import JSONDecodeError
from pathlib import Path
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
        Path(".config", "op", "config"),
        Path(".op", "config")
    ]

    def __init__(self, configpath=None, logger: logging.Logger = None):
        super().__init__()
        if not logger:
            logger = logging.getLogger(self.__class__.__name__)
            logger.setLevel(logging.INFO)
        self.logger = logger
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

    def _get_custom_config_dir(self, custom_config_dir: str | Path):
        if not custom_config_dir:
            op_conf_dir = os.environ.get("OP_CONFIG_DIR", None)
            if op_conf_dir:
                custom_config_dir = Path(op_conf_dir)
                self.logger.debug(f"OP_CONFIG_DIR set to: {custom_config_dir}")
        else:
            self.logger.debug(
                f"Custom config dir specified: {custom_config_dir}")
        return custom_config_dir

    def _get_config_path(self) -> Path:
        configpath: Path = None
        config_home = None
        try:
            config_home = Path(os.environ['XDG_CONFIG_HOME'])

        except KeyError:
            config_home = Path.home()

        for subpath in self.OP_CONFIG_PATHS:
            _configpath = Path(config_home, subpath)
            self.logger.debug(f"Looking for config at {_configpath}")
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
