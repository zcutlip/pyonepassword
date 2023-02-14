import os

import pytest

from pyonepassword._op_cli_config import OPCLIConfig
from pyonepassword.api.exceptions import OPConfigNotFoundException

from .fixtures.expected_op_cli_config import ExpectedConfigData
from .fixtures.platform_support import DEV_NULL, HOME_ENV_VAR, is_windows


def _sanity_check_xdg_home_env():
    assert os.environ.get('XDG_CONFIG_HOME') is not None
    assert os.environ.get(HOME_ENV_VAR) in [DEV_NULL, None]


def _sanity_check_standard_home_env():
    assert os.environ.get('XDG_CONFIG_HOME') is None
    assert os.environ.get(HOME_ENV_VAR) not in [DEV_NULL, None]


def test_op_cli_config_homedir_01(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_homedir):
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.shorthand == expected.shorthand


def test_op_cli_config_homedir_02(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_homedir):
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.account_uuid == expected.account_uuid


def test_op_cli_config_homedir_03(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_homedir):
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.url == expected.url


def test_op_cli_config_homedir_04(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_homedir):
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.user_uuid == expected.user_uuid


def test_op_cli_config_homedir_05(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_homedir):
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.email == expected.email


def test_op_cli_config_homedir_06(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_homedir):
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.uuid_for_account("example_shorthand")
    assert result == expected.user_uuid


def test_op_cli_config_homedir_07(valid_op_cli_config_homedir):
    _sanity_check_standard_home_env()
    shorthand = "NO_SUCH_SHORTHAND"
    config = OPCLIConfig()
    with pytest.raises(OPConfigNotFoundException):
        config.get_config(shorthand)


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
def test_op_cli_config_alt_acct_identifiers_01(expected_op_config_data: ExpectedConfigData):
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    user_uuid = "5GHHPJK5HZC5BAT7WDUXW57G44"
    config = OPCLIConfig()
    result = config.get_config(user_uuid)
    assert expected.user_uuid == result.user_uuid


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
def test_op_cli_config_alt_acct_identifiers_02(expected_op_config_data: ExpectedConfigData):
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    user_email = "example_user@example.email"
    config = OPCLIConfig()
    result = config.get_config(user_email)
    assert expected.user_uuid == result.user_uuid


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
def test_op_cli_config_alt_acct_identifiers_03(expected_op_config_data: ExpectedConfigData):
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    account_uuid = "GRXJAN4BY5DPROISKYL55IRCPY"
    config = OPCLIConfig()
    result = config.get_config(account_uuid)
    assert expected.user_uuid == result.user_uuid


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
def test_op_cli_config_alt_acct_identifiers_04(expected_op_config_data: ExpectedConfigData):
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    account_url = "https://example-account.1password.com"
    config = OPCLIConfig()
    result = config.get_config(account_url)
    assert expected.user_uuid == result.user_uuid


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
    result = config.uuid_for_account("example_shorthand")
    assert result == expected.user_uuid


def test_op_cli_config_xdg_07(expected_op_config_data: ExpectedConfigData, valid_op_cli_config_xdghome):
    shorthand = "NO_SUCH_SHORTHAND"
    config = OPCLIConfig()
    with pytest.raises(OPConfigNotFoundException):
        config.get_config(shorthand)


def test_op_cli_config_unreable_01(invalid_op_cli_config_unreable):
    # NOTE: This test will fail if run as root (e.g., in a docker container with no users)
    # there is no way to make a file unreadable to root
    if not is_windows():
        # this test depends on creating a config file that's not readable
        # this is not straightforward on windows via native python APIs
        # so only run this test if not on windows
        with pytest.raises(OPConfigNotFoundException):
            OPCLIConfig()
    else:
        assert True


def test_op_cli_config_missing_01(invalid_op_cli_config_missing):
    with pytest.raises(OPConfigNotFoundException):
        OPCLIConfig()


def test_op_cli_config_missing_02(invalid_op_cli_config_missing):
    with pytest.raises(OPConfigNotFoundException):
        OPCLIConfig(configpath="no_such_path")


def test_op_cli_config_malformed_01(invalid_op_cli_config_malformed):
    with pytest.raises(OPConfigNotFoundException):
        OPCLIConfig()


def test_op_cli_config_missing_shorthand_01(valid_op_cli_config_no_shorthand):
    conf = OPCLIConfig()
    with pytest.raises(OPConfigNotFoundException):
        conf.get_config()


@pytest.mark.usefixtures("valid_op_cli_config_no_account_list")
# @pytest.mark.usefixtures("setup_normal_op_env")
def test_op_cli_config_no_account_list_01():
    """
    Verify we can instantiate OPCLIConfig() even when account list is null
    """
    OPCLIConfig()
