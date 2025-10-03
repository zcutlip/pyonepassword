"""
Test fixture for validating OP CLI configuration.

This module provides a test fixture class that sets up a temporary environment
with a valid OP CLI configuration for testing purposes. It creates a temporary
directory to simulate a user's home directory, sets environment variables to
redirect OP CLI configuration paths, and creates a valid configuration file
with test data.

The fixture is designed to be used in unit tests to ensure that the OP CLI
configuration handling works correctly without affecting the user's actual
configuration.
"""

import os
import tempfile
from enum import IntEnum
from pathlib import Path

from pyonepassword import logging

# "home" environment variable is different on Windows vs Linux/Unix
from .platform_support import HOME_ENV_VAR
from .valid_data import ValidData

VALID_OP_CONFIG_KEY = "example-op-config"
VALID_OP_CONFIG_NO_SHORTHAND_KEY = "example-op-config-no-latest-shorthand"
VALID_OP_CONFIG_NO_ACCOUNT_LIST_KEY = "example-op-config-no-account-list"


class ConfigPathType(IntEnum):
    ENV_OP_CONFIG_DIR = 2  # OP_CONFIG_DIR=/path/to/conf/dir/
    HOME_DOT_OP = 3  # ~/.op
    XDG_CONF_DOT_OP = 4  # ${XDG_CONFIG_HOME}/.op
    HOME_DOT_CONFIG_OP = 5  # ${HOME}/.config/op
    XDG_CONF_OP = 6  # ${XDG_CONFIG_HOME}/op


class ValidOPCLIConfig:
    """Test fixture for validating OP CLI configuration.

    This class sets up a temporary environment with a valid OP CLI configuration
    for testing purposes. It creates a temporary directory to simulate a user's
    home directory, sets environment variables to redirect OP CLI configuration
    paths, and creates a valid configuration file with test data.

    The fixture is designed to be used in automated tests to ensure that
    provide a valid 'op' CLI configuration without conflicting with the user's
    actual configuration, if one exists.
    """

    def __init__(self,
                 location_env_var=HOME_ENV_VAR,
                 config_text=None,
                 valid_data_key=VALID_OP_CONFIG_KEY,
                 logger=None,
                 config_path_type: ConfigPathType | None = None):
        """Initialize the test fixture for OP CLI configuration.

        Args:
            location_env_var (str, optional): The environment variable to use for
                setting the configuration location. Defaults to HOME_ENV_VAR.
            config_text (str, optional): The configuration text to write to the
                config file. If None, uses test data from ValidData. Defaults to None.
            valid_data_key (str, optional): The key to use when retrieving test data
                from ValidData. Defaults to VALID_OP_CONFIG_KEY.
            logger (logging.Logger, optional): The logger instance to use. If None,
                creates a console logger with WARNING level. Defaults to None.
            config_path_type (str, optional): The type of config path to create.
                Can be one of: 'op_config_dir', 'home_op', 'xdg_home_op',
                'home_config_op', 'xdg_config_op', or None for default.
                Defaults to None.

        Behavior:
            - Creates a temporary directory to simulate a user's home directory, and contain a valid 'op' config
            - Sets environment variables to redirect OP CLI configuration paths
            - Creates a valid configuration file with test data
            - Restores environment variables when destroyed
        """
        if not logger:
            logger = logging.console_logger("pytest", logging.WARNING)
        self.logger = logger
        self._new_home = None
        self._old_home = None
        self._tempdir = tempfile.TemporaryDirectory()
        """
        The rules are applied in order:
        1. A directory specified with config_dir
        2. A directory set with the OP_CONFIG_DIR environment variable
        3. ~/.op
        4. ${XDG_CONFIG_HOME}/.op
        5. ~/.config/op
        6. ${XDG_CONFIG_HOME}/op
        """
        # reset $HOME to something useless
        # of location_env_var is HOME, we'll reset it later
        new_home = os.devnull

        # in some environments HOME may not be set, so don't assume it is
        self._old_home = os.environ.get(HOME_ENV_VAR)
        self._old_xdg = os.environ.get("XDG_CONFIG_HOME")
        if self._old_home is not None:
            os.environ[HOME_ENV_VAR] = new_home

        if location_env_var is not None:
            os.environ[location_env_var] = self._tempdir.name
        # save whatever we set HOME to for later comparison & restore
        self._new_home = os.environ.get(HOME_ENV_VAR)
        self._new_xdg = os.environ.get('XDG_CONFIG_HOME')

        if location_env_var != "XDG_CONFIG_HOME":
            # if we didn't explicitly need XDG_CONFIG_HOME, make sure it hasn't been set
            os.environ.pop('XDG_CONFIG_HOME', None)

        old_umask = os.umask(0o077)

        # Create config file at the appropriate location based on the environment variables
        op_config_path = self._create_config_at_appropriate_location(
            config_path_type)
        self.logger.debug(f"valid config path: {op_config_path}")
        if config_text is None:
            config_text = ValidData().data_for_name(valid_data_key)

        if not isinstance(config_text, str):
            raise TypeError("config_text must be a string")

        with open(op_config_path, "w") as config:
            config.write(config_text)
        os.umask(old_umask)
        self._op_config_path = op_config_path

    def __del__(self):
        """
        Restores the original environment variables (HOME and XDG_CONFIG_HOME)
        to their previous values when the fixture is destroyed.

        Behavior:
            - Restores the original HOME environment variable if it had been set
            - Restores the original XDG_CONFIG_HOME environment variable if it was modified
            - Cleans up the temporary directory
        """
        if os.environ.get(HOME_ENV_VAR) == self._new_home:
            if self._old_home is not None:
                os.environ[HOME_ENV_VAR] = self._old_home
            else:
                os.environ.pop(HOME_ENV_VAR, None)

        if os.environ.get('XDG_CONFIG_HOME') == self._new_xdg:
            if self._old_xdg is not None:
                os.environ['XDG_CONFIG_HOME'] = self._old_xdg
            else:
                # we can't set an env variable to None. You have to delete it
                os.environ.pop('XDG_CONFIG_HOME', None)

    def _create_config_at_appropriate_location(self,
                                               config_path_type: ConfigPathType | None = None) -> Path:
        """
        Create a config file at the appropriate location based on environment variables.

        The rules are applied in order:
        1. A directory specified with config_dir
        2. A directory set with the OP_CONFIG_DIR environment variable
        3. ~/.op
        4. ${XDG_CONFIG_HOME}/.op
        5. ~/.config/op
        6. ${XDG_CONFIG_HOME}/op

        For testing purposes, we simulate these by checking which environment variable
        is set and creating the config file in the appropriate location within our
        temporary directory.

        Args:
            config_path_type (str, optional): The type of config path to create.
                Can be one of: 'op_config_dir', 'home_op', 'xdg_home_op',
                'home_config_op', 'xdg_config_op', or None for default.
        """
        if config_path_type == ConfigPathType.ENV_OP_CONFIG_DIR:
            # Rule 2: A directory set with the OP_CONFIG_DIR environment variable
            op_config_dir = os.environ.get("OP_CONFIG_DIR")
            if not op_config_dir:
                # If not set, create a custom directory for testing
                op_config_dir = Path(self._tempdir.name, "custom_op_config")
                os.environ["OP_CONFIG_DIR"] = str(op_config_dir)
            config_path = Path(op_config_dir, "config")
            config_path.parent.mkdir(parents=True, exist_ok=True)
            return config_path

        elif config_path_type == ConfigPathType.HOME_DOT_OP:
            # Rule 3: ~/.op
            home_op_path = Path(self._tempdir.name, ".op")
            home_op_path.mkdir(parents=True, exist_ok=True)
            config_path = Path(home_op_path, "config")
            return config_path

        elif config_path_type == ConfigPathType.XDG_CONF_DOT_OP:
            # Rule 4: ${XDG_CONFIG_HOME}/.op
            xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
            if not xdg_config_home:
                # If not set, create a custom XDG directory for testing
                xdg_config_home = Path(self._tempdir.name, "xdg_config")
                os.environ["XDG_CONFIG_HOME"] = str(xdg_config_home)
            xdg_op_path = Path(xdg_config_home, ".op")
            xdg_op_path.mkdir(parents=True, exist_ok=True)
            config_path = Path(xdg_op_path, "config")
            return config_path

        elif config_path_type == ConfigPathType.HOME_DOT_CONFIG_OP:
            # Rule 5: ~/.config/op
            config_dir = Path(self._tempdir.name, ".config", "op")
            config_dir.mkdir(parents=True, exist_ok=True)
            config_path = Path(config_dir, "config")
            return config_path

        elif config_path_type == ConfigPathType.XDG_CONF_OP:
            # Rule 6: ${XDG_CONFIG_HOME}/op
            xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
            if not xdg_config_home:
                # If not set, create a custom XDG directory for testing
                xdg_config_home = Path(self._tempdir.name, "xdg_config")
                os.environ["XDG_CONFIG_HOME"] = str(xdg_config_home)
            xdg_op_path = Path(xdg_config_home, "op")
            xdg_op_path.mkdir(parents=True, exist_ok=True)
            config_path = Path(xdg_op_path, "config")
            return config_path

        else:
            # Default behavior - check environment variables and apply rules in order
            # Check if OP_CONFIG_DIR is set (Rule 2)
            op_config_dir = os.environ.get("OP_CONFIG_DIR")
            if op_config_dir:
                config_path = Path(op_config_dir, "config")
                config_path.parent.mkdir(parents=True, exist_ok=True)
                return config_path

            # Check if we're using XDG_CONFIG_HOME for ~/.op (Rule 4)
            xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
            if xdg_config_home:
                xdg_op_path = Path(xdg_config_home, ".op", "config")
                xdg_op_path.parent.mkdir(parents=True, exist_ok=True)
                return xdg_op_path

            # Default to ~/.config/op (Rule 5)
            config_dir = Path(self._tempdir.name, ".config", "op")
            config_dir.mkdir(parents=True, exist_ok=True)
            config_path = Path(config_dir, "config")
            return config_path
