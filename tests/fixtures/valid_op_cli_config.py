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
    configuration environment, sets environment variables according to the
    specified ConfigPathType, and creates a valid configuration file with test data.

    The fixture is designed to be used in automated tests to ensure that
    pyonepassword can correctly locate and use 'op' CLI configuration files
    in different locations without conflicting with the user's actual configuration.
    """

    def __init__(self,
                 monkeypatch,
                 config_text=None,
                 valid_data_key=VALID_OP_CONFIG_KEY,
                 logger=None,
                 config_path_type: ConfigPathType | None = None):
        """Initialize the test fixture for OP CLI configuration.

        Args:
            monkeypatch (pytest.monkeypatch): Pytest monkeypatch fixture for
                setting environment variables. Required parameter.
            config_text (str, optional): The configuration text to write to the
                config file. If None, uses test data from ValidData. Defaults to None.
            valid_data_key (str, optional): The key to use when retrieving test data
                from ValidData. Defaults to VALID_OP_CONFIG_KEY.
            logger (logging.Logger, optional): The logger instance to use. If None,
                creates a console logger with WARNING level. Defaults to None.
            config_path_type (ConfigPathType, optional): The type of config path to create.
                Should be one of the ConfigPathType enum values or None for default.
                Defaults to None.

        Behavior:
            - Creates a temporary directory to simulate a user's configuration environment
            - Sets environment variables according to the specified config_path_type
            - Creates a valid configuration file with test data
            - Restores environment variables when destroyed
        """
        if not logger:
            logger = logging.console_logger(
                "ValidOPCLIConfig", logging.WARNING)
        self.logger = logger
        self._tempdir = tempfile.TemporaryDirectory()
        self._monkeypatch = monkeypatch

        # Set up environment variables based on config_path_type
        self._setup_environment_variables(config_path_type)

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

    def _setup_environment_variables(self, config_path_type: ConfigPathType | None):
        """
        Set up environment variables according to the specified config_path_type.

        Args:
            config_path_type (ConfigPathType, optional): The type of config path to create.
                Should be one of the ConfigPathType enum values or None for default.
        """
        if config_path_type is None:
            config_path_type = ConfigPathType.HOME_DOT_OP

        mp = self._monkeypatch

        if os.environ.get(HOME_ENV_VAR) is not None:
            mp.setenv(HOME_ENV_VAR, os.devnull)

        if config_path_type == ConfigPathType.ENV_OP_CONFIG_DIR:
            # For OP_CONFIG_DIR, we set a custom directory and don't set HOME
            op_config_dir = Path(self._tempdir.name, "custom_op_config")
            op_config_dir.mkdir(parents=True, exist_ok=True)
            mp.setenv("OP_CONFIG_DIR", str(op_config_dir))

        elif config_path_type == ConfigPathType.HOME_DOT_OP:
            # For ~/.op, set HOME to our temporary directory
            mp.setenv(HOME_ENV_VAR, self._tempdir.name)

        elif config_path_type == ConfigPathType.XDG_CONF_DOT_OP:
            # For ${XDG_CONFIG_HOME}/.op, set XDG_CONFIG_HOME to our temporary directory
            xdg_config_home = Path(self._tempdir.name, "xdg_config_home")
            xdg_config_home.mkdir(parents=True, exist_ok=True)
            mp.setenv("XDG_CONFIG_HOME", str(xdg_config_home))

        elif config_path_type == ConfigPathType.HOME_DOT_CONFIG_OP:
            # For ~/.config/op, set HOME to our temporary directory (default behavior)
            mp.setenv(HOME_ENV_VAR, self._tempdir.name)

        elif config_path_type == ConfigPathType.XDG_CONF_OP:
            # For ${XDG_CONFIG_HOME}/op, set XDG_CONFIG_HOME to our temporary directory
            xdg_config_home = Path(self._tempdir.name, "xdg_config_home")
            xdg_config_home.mkdir(parents=True, exist_ok=True)
            mp.setenv("XDG_CONFIG_HOME", str(xdg_config_home))

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

        For testing purposes, we create the config file in the appropriate location
        within our temporary directory based on the config_path_type.

        Args:
            config_path_type (ConfigPathType, optional): The type of config path to create.
                Should be one of the ConfigPathType enum values or None for default.
        """
        if config_path_type is None:
            config_path_type = ConfigPathType.HOME_DOT_OP

        if config_path_type == ConfigPathType.ENV_OP_CONFIG_DIR:
            # Rule 2: A directory set with the OP_CONFIG_DIR environment variable
            op_config_dir = os.environ.get("OP_CONFIG_DIR")
            if not op_config_dir:
                raise RuntimeError(
                    "OP_CONFIG_DIR should have been set by _setup_environment_variables")
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
                raise RuntimeError(
                    "XDG_CONFIG_HOME should have been set by _setup_environment_variables")
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
                raise RuntimeError(
                    "XDG_CONFIG_HOME should have been set by _setup_environment_variables")
            xdg_op_path = Path(xdg_config_home, "op")
            xdg_op_path.mkdir(parents=True, exist_ok=True)
            config_path = Path(xdg_op_path, "config")
            return config_path
