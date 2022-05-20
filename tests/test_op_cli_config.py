import os

import pytest

from pyonepassword._op_cli_config import OPCLIConfig
from pyonepassword.py_op_exceptions import OPConfigNotFoundException

from .fixtures.expected_op_cli_config import ExpectedConfigData


def _sanity_check_xdg_home_env():
    assert os.environ['XDG_CONFIG_HOME'] is not None
    assert os.environ['HOME'] == '/dev/null'


def test_op_cli_config_homedir_01(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_homedir):
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.shorthand == expected.shorthand


def test_op_cli_config_homedir_02(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_homedir):
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.account_uuid == expected.account_uuid


def test_op_cli_config_homedir_03(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_homedir):
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.url == expected.url


def test_op_cli_config_homedir_04(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_homedir):
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.user_uuid == expected.user_uuid


def test_op_cli_config_homedir_05(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_homedir):
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.email == expected.email


def test_op_cli_config_homedir_06(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_homedir):
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.uuid_for_shorthand("example_shorthand")
    assert result == expected.user_uuid


def test_op_cli_config_homedir_07(valid_op_cli_config_homedir):
    shorthand = "NO_SUCH_SHORTHAND"
    config = OPCLIConfig()
    with pytest.raises(OPConfigNotFoundException):
        config.get_config(shorthand)


def test_op_cli_config_xdg_01(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_xdghome):
    _sanity_check_xdg_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.shorthand == expected.shorthand


def test_op_cli_config_xdg_02(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_xdghome):
    _sanity_check_xdg_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.account_uuid == expected.account_uuid


def test_op_cli_config_xdg_03(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_xdghome):
    _sanity_check_xdg_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.url == expected.url


def test_op_cli_config_xdg_04(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_xdghome):
    _sanity_check_xdg_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.user_uuid == expected.user_uuid


def test_op_cli_config_xdg_05(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_xdghome):
    _sanity_check_xdg_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.email == expected.email


def test_op_cli_config_xdg_06(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_xdghome):
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.uuid_for_shorthand("example_shorthand")
    assert result == expected.user_uuid


def test_op_cli_config_xdg_07(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_xdghome):
    shorthand = "NO_SUCH_SHORTHAND"
    config = OPCLIConfig()
    with pytest.raises(OPConfigNotFoundException):
        config.get_config(shorthand)
