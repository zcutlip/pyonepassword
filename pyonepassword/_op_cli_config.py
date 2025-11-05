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

    def __init__(self, config_dir: Optional[str | Path] = None, logger: Optional[logging.Logger] = None):
        super().__init__()
        if not logger:
            logger = logging.getLogger(self.__class__.__name__)
            logger.setLevel(logging.INFO)
        self.logger = logger

        configpath = self._get_config_path(config_dir=config_dir)
        self.logger.debug(f"configpath: {configpath}")
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

    def _get_config_path(self, config_dir=None) -> Path | None:
        """
        Determine the path to the 1Password CLI configuration file.

        This method follows the 1Password CLI configuration directory rules
        to determine the order in which configuration files should be checked.
        The rules are applied in order:
        1. A directory specified with config_dir
        2. A directory set with the OP_CONFIG_DIR environment variable
        3. ~/.op
        4. ${XDG_CONFIG_HOME}/.op
        5. ~/.config/op
        6. ${XDG_CONFIG_HOME}/op

        NOTE: If a custom configuration directory is provided or OP_CONFIG_DIR is set,
        their use is mandatory and there is no fallback if the config file isn't present.

        Args:
            config_dir: Optional custom configuration directory path.
                        If provided, this will be used as the base directory
                        for locating the config file.

        Returns:
            Path: The path to the configuration file if found, otherwise None.
        """
        configpath: Path | None = None
        path_options = self._config_path_triage_list(config_dir)
        for _configpath in path_options:
            self.logger.debug(f"Looking for config at {_configpath}")
            if _configpath.exists():
                configpath = _configpath
                break

        return configpath

    def _get_custom_config_dir(self, custom_config_dir: str | Path) -> Path | None:
        """
        Determine the custom configuration directory path if one has been specified.

        If the user has specified a custom configuration directory, we must use that,
        and there's no fallback if it doesn't exist.

        NOTE: This is a configuration directory. A config file named "config" will be
        looked for inside.

        This can take the form of (in order):
        - explicitly provided
        - set in OP_CONFIG_DIR env variable.

        Args:
            custom_config_dir: The custom configuration directory path, if provided.

        Returns:
            Path: The custom configuration directory path, or None if not specified.
        """
        config_dir_return: Path | None = None
        if not custom_config_dir:
            op_conf_dir = os.environ.get("OP_CONFIG_DIR", None)
            if op_conf_dir:
                config_dir_return = Path(op_conf_dir)
                self.logger.debug(f"OP_CONFIG_DIR set to: {custom_config_dir}")
        else:
            config_dir_return = Path(custom_config_dir)
            self.logger.debug(
                f"Custom config dir specified: {custom_config_dir}")
        return config_dir_return

    def _config_path_triage_list(self, custom_config_dir) -> list[Path]:
        """
        Generate a list of potential configuration file paths to check.


        Args:
            custom_config_dir: The custom configuration directory path, if provided.

        Returns:
            list[Path]: A list of potential configuration file paths to check,
                       in order of preference.
        """
        xdg_home = os.environ.get('XDG_CONFIG_HOME', None)
        if xdg_home:
            self.logger.debug(f"XDG_CONFIG_HOME set to {xdg_home}")
        custom_config_dir = self._get_custom_config_dir(custom_config_dir)
        configpath = None
        path_options: list[Path] = []
        # Rules from https://developer.1password.com/docs/cli/config-directories/
        if custom_config_dir:
            # rule 1: A directory specified with --config
            # rule 2: A directory set with the OP_CONFIG_DIR environment variable.
            configpath = Path(custom_config_dir, "config")
            self.logger.debug(
                f"Rule 1 & 2: Adding custom_config_dir to path triage list: {configpath}")

            if not configpath.exists():
                # we were explicitly told to use this path, so there's no fallback
                # if it doesn't exist
                raise OPConfigNotFoundException(
                    f"Caller-provided config not found at {configpath}")
            else:
                path_options.append(configpath)

        else:
            # rule 1 or 2 weren't met, so we evaluate the rest
            # rule 3: ~/.op (following go-homedir  to determine the home directory)
            # We use pathlib.Path.expanduser(). Hopefully this matches go-homedir semantics
            self.logger.debug("Rule 3: adding ~/.op to path triage list")
            config_dir = Path("~/.op").expanduser()
            config_path = Path(config_dir, "config")
            path_options.append(config_path)

            # rule 4: ${XDG_CONFIG_HOME}/.op
            if xdg_home:
                self.logger.debug(
                    "Rule 4: Adding ${XDG_CONFIG_HOME}/.op to path triage list")
                config_path = Path(xdg_home, ".op", "config")
                path_options.append(config_path)

            # rule 5: ~/.config/op (following go-homedir to determine the home directory)
            self.logger.debug(
                "Rule 5: Adding ~/.config/op to path triage list")
            config_dir = Path("~/.config", "op").expanduser()
            config_path = Path(config_dir, "config")
            path_options.append(config_path)

            # rule 6: ${XDG_CONFIG_HOME}/op
            if xdg_home:
                self.logger.debug(
                    "Rule 6: Adding ${XDG_CONFIG_HOME}/op to path triage list")
                config_path = Path(xdg_home, "op", "config")
                path_options.append(config_path)

        return path_options

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
