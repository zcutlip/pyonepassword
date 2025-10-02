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
from pathlib import Path

from pyonepassword import logging

# "home" environment variable is different on Windows vs Linux/Unix
from .platform_support import HOME_ENV_VAR
from .valid_data import ValidData

VALID_OP_CONFIG_KEY = "example-op-config"
VALID_OP_CONFIG_NO_SHORTHAND_KEY = "example-op-config-no-latest-shorthand"
VALID_OP_CONFIG_NO_ACCOUNT_LIST_KEY = "example-op-config-no-account-list"


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

    def __init__(self, location_env_var=HOME_ENV_VAR, config_text=None, valid_data_key=VALID_OP_CONFIG_KEY, logger=None):
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

        if not self._new_xdg:
            op_config_path = Path(self._tempdir.name, ".config")
        op_config_path = Path(self._tempdir.name, "op")
        op_config_path.mkdir(parents=True)
        op_config_path = Path(op_config_path, "config")
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
