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


# LOCATION TESTS - NORMAL OPERATIONS

@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_op_cli_config_homedir_01(expected_op_config_data: ExpectedConfigData):
    """
    Stage:
        A valid op config in the default location under "$HOME" (rule 3)

    Create:
        OPCLIConfig object with default parameters

    Verify:
        The resulting object's shorthand property matches th expected shorthand value
    """
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.shorthand == expected.shorthand


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_op_cli_config_homedir_02(expected_op_config_data: ExpectedConfigData):
    """
    Stage:
        A valid op config in the default location under "$HOME" (rule 3)

    Create:
        OPCLIConfig object with default parameters

    Verify:
        The resulting object's account_uuid property matches the expected account UUID value
    """
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.account_uuid == expected.account_uuid


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_op_cli_config_homedir_03(expected_op_config_data: ExpectedConfigData):
    """
    Stage:
        A valid op config in the default location under "$HOME" (rule 3)

    Create:
        OPCLIConfig object with default parameters

    Verify:
        The resulting object's url property matches the expected URL value
    """
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.url == expected.url


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_op_cli_config_homedir_04(expected_op_config_data: ExpectedConfigData):
    """
    Stage:
        A valid op config in the default location under "$HOME" (rule 3)

    Create:
        OPCLIConfig object with default parameters

    Verify:
        The resulting object's user_uuid property matches the expected user UUID value
    """
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.user_uuid == expected.user_uuid


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_op_cli_config_homedir_05(expected_op_config_data: ExpectedConfigData):
    """
    Stage:
        A valid op config in the default location under "$HOME" (rule 3)

    Create:
        OPCLIConfig object with default parameters

    Verify:
        The resulting object's email property matches the expected email value
    """
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.email == expected.email


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_op_cli_config_homedir_06(expected_op_config_data: ExpectedConfigData):
    """
    Stage:
        A valid op config in the default location under "$HOME" (rule 3)

    Create:
        OPCLIConfig object with default parameters

    Verify:
        The uuid_for_account() method returns the expected user UUID value
    """
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.uuid_for_account("example_shorthand")
    assert result == expected.user_uuid


@pytest.mark.usefixtures("valid_op_cli_config_xdghome")
def test_op_cli_config_xdg_01(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config in ${XDG_CONFIG_HOME}/.op location (rule 4)
        XDG_CONFIG_HOME is set, HOME is set to /dev/null

    Create:
        OPCLIConfig object

    Verify:
        The resulting object's shorthand property matches the expected shorthand value
    """
    _sanity_check_xdg_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand")
    assert result.shorthand == expected.shorthand


@pytest.mark.usefixtures("valid_op_cli_config_xdghome")
def test_op_cli_config_xdg_02(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config in ${XDG_CONFIG_HOME}/.op location (rule 4)
        XDG_CONFIG_HOME is set, HOME is set to /dev/null

    Create:
        OPCLIConfig object

    Verify:
        The resulting object's account_uuid property matches the expected account UUID value
    """
    _sanity_check_xdg_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand")
    assert result.account_uuid == expected.account_uuid


@pytest.mark.usefixtures("valid_op_cli_config_xdghome")
def test_op_cli_config_xdg_03(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config in ${XDG_CONFIG_HOME}/.op location (rule 4)
        XDG_CONFIG_HOME is set, HOME is set to /dev/null

    Create:
        OPCLIConfig object

    Verify:
        The resulting object's url property matches the expected URL value
    """
    _sanity_check_xdg_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand")
    assert result.url == expected.url


@pytest.mark.usefixtures("valid_op_cli_config_xdghome")
def test_op_cli_config_xdg_04(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config in ${XDG_CONFIG_HOME}/.op location (rule 4)
        XDG_CONFIG_HOME is set, HOME is set to /dev/null

    Create:
        OPCLIConfig object

    Verify:
        The resulting object's user_uuid property matches the expected user UUID value
    """
    _sanity_check_xdg_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand")
    assert result.user_uuid == expected.user_uuid


@pytest.mark.usefixtures("valid_op_cli_config_xdghome")
def test_op_cli_config_xdg_05(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config in ${XDG_CONFIG_HOME}/.op location (rule 4)
        XDG_CONFIG_HOME is set, HOME is set to /dev/null

    Create:
        OPCLIConfig object

    Verify:
        The resulting object's email property matches the expected email value
    """
    _sanity_check_xdg_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand")
    assert result.email == expected.email


@pytest.mark.usefixtures("valid_op_cli_config_xdghome")
def test_op_cli_config_xdg_06(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config in ${XDG_CONFIG_HOME}/.op location (rule 4)
        XDG_CONFIG_HOME is set, HOME is set to /dev/null

    Create:
        OPCLIConfig object

    Verify:
        The uuid_for_account() method returns the expected user UUID value
    """
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig(logger=console_logger)
    result = config.uuid_for_account("example_shorthand")
    assert result == expected.user_uuid


@pytest.mark.usefixtures("valid_op_cli_config_op_config_dir")
def test_op_cli_config_op_config_dir_01(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        Set OP_CONFIG_DIR environment variable
        A valid op config in OP_CONFIG_DIR location (rule 2)

    Create:
        OPCLIConfig object

    Verify:
        The resulting object's shorthand and account_uuid properties match expected values
        Tests that OP_CONFIG_DIR environment variable config location works correctly
    """
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand")
    assert result.shorthand == expected.shorthand
    assert result.account_uuid == expected.account_uuid


@pytest.mark.usefixtures("valid_op_cli_config_home_config_op")
def test_op_cli_config_home_config_op_01(expected_op_config_data: ExpectedConfigData):
    """
    Stage:
        A valid op config in ~/.config/op location (rule 5)

    Create:
        OPCLIConfig object

    Verify:
        The resulting object's shorthand and account_uuid properties match expected values
        Tests that explicit ~/.config/op config location works correctly
    """
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.shorthand == expected.shorthand
    assert result.account_uuid == expected.account_uuid


@pytest.mark.usefixtures("valid_op_cli_config_xdg_config_op")
def test_op_cli_config_xdg_config_op_01(expected_op_config_data: ExpectedConfigData):
    """
    Stage:
        A valid op config in ${XDG_CONFIG_HOME}/op location (rule 6)

    Create:
        OPCLIConfig object

    Verify:
        The resulting object's shorthand and account_uuid properties match expected values
        Tests that explicit ${XDG_CONFIG_HOME}/op config location works correctly
    """
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig()
    result = config.get_config("example_shorthand")
    assert result.shorthand == expected.shorthand
    assert result.account_uuid == expected.account_uuid


# ALTERNATIVE IDENTIFIER TESTS

@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
def test_op_cli_config_alt_acct_identifiers_01(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config with no latest sign-in/shorthand
        in the default location under "$HOME" (rule 3)

    Create:
        OPCLIConfig object with default parameters

    Verify:
        - The resulting object's get_config method works with a user_uuid identifier
            even when the config file has no latest sign-in value
        - The resulting user UUID matches the expected UUID
    """
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    user_uuid = "5GHHPJK5HZC5BAT7WDUXW57G44"
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config(user_uuid)
    assert expected.user_uuid == result.user_uuid


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
def test_op_cli_config_alt_acct_identifiers_02(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config with no latest sign-in/shorthand in the default location under "$HOME" (rule 3)

    Create:
        OPCLIConfig object with default parameters

    Verify:
        The resulting object's user_uuid property matches the expected user UUID value when
        get_config() is called with a user email identifier
    """
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    user_email = "example_user@example.email"
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config(user_email)
    assert expected.user_uuid == result.user_uuid


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
def test_op_cli_config_alt_acct_identifiers_03(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config with no latest sign-in/shorthand
        in the default location under "$HOME"

    Create:
        OPCLIConfig object with default parameters

    Verify:
        The resulting object's user_uuid property matches the expected user UUID value when
        get_config() is called with an account UUID identifier
    """
    _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    account_uuid = "GRXJAN4BY5DPROISKYL55IRCPY"
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config(account_uuid)
    assert expected.user_uuid == result.user_uuid


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
def test_op_cli_config_alt_acct_identifiers_04(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config with no latest sign-in/shorthand
        in the default location under "$HOME"

    Create:
        OPCLIConfig object with default parameters

    Verify:
        The resulting object's user_uuid property matches the expected user UUID value when
        get_config() is called with an account URL identifier
    """
    _sanity_check_standard_home_env()
    console_logger.info("pytest console logger")
    expected = expected_op_config_data.data_for_key("example-account")
    account_url = "https://example-account.1password.com"
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config(account_url)
    assert expected.user_uuid == result.user_uuid


# SEARCH PRIORITY TESTS

@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("invalid_op_cli_config_malformed_xdg_config_op")
def test_op_cli_config_valid_and_malformed_01(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config in ~/.op location (rule 3)
        AND a malformed op config in ${XDG_CONFIG_HOME}/op location (rule 6)

    Create:
        OPCLIConfig object

    Verify:
        The valid config (rule 3) is found and used before the malformed config (rule 6)
        Tests config search order priority
    """
    # _sanity_check_standard_home_env()
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand")
    assert result.account_uuid == expected.account_uuid


@pytest.mark.usefixtures("invalid_op_cli_malformed_config_homedir")
@pytest.mark.usefixtures("valid_op_cli_config_xdg_config_op")
def test_op_cli_config_valid_and_malformed_02(console_logger):
    """
    Stage:
        A malformed op config in ~/.config/op location (rule 5)
        AND a valid op config in ${XDG_CONFIG_HOME}/op location (rule 6)

    Create:
        OPCLIConfig object

    Verify:
        OPConfigNotFoundException is raised because malformed config (rule 5) is encountered
        before valid config (rule 6) in search order
        Tests config search order priority
    """
    # _sanity_check_standard_home_env()
    with pytest.raises(OPConfigNotFoundException):
        OPCLIConfig(logger=console_logger)


# SEARCH PRIORITY TESTS WITH TWO VALID CONFIGS

@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("valid_op_cli_config_xdg_config_op_account_2")
def test_op_cli_config_two_valid_01(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config in ~/.op location (rule 3) with example-account data
        AND a valid op config in ${XDG_CONFIG_HOME}/op location (rule 6) with example-account-2 data

    Create:
        OPCLIConfig object

    Verify:
        The config from rule 3 (~/.op) is found and used before the config from rule 6
        Tests config search order priority when both configs are valid
        Verifies the higher priority config (example-account) is loaded
    """
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand")
    assert result.shorthand == expected.shorthand
    assert result.account_uuid == expected.account_uuid
    assert result.email == expected.email
    assert result.url == expected.url


@pytest.mark.usefixtures("valid_op_cli_config_xdghome")
@pytest.mark.usefixtures("valid_op_cli_config_home_config_op_account_2")
def test_op_cli_config_two_valid_02(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config in ${XDG_CONFIG_HOME}/.op location (rule 4) with example-account data
        AND a valid op config in ~/.config/op location (rule 5) with example-account-2 data

    Create:
        OPCLIConfig object

    Verify:
        The config from rule 4 (${XDG_CONFIG_HOME}/.op) is found and used before the config from rule 5
        Tests config search order priority when both configs are valid
        Verifies the higher priority config (example-account) is loaded
    """
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand")
    assert result.shorthand == expected.shorthand
    assert result.account_uuid == expected.account_uuid
    assert result.email == expected.email
    assert result.url == expected.url


@pytest.mark.usefixtures("valid_op_cli_config_home_config_op")
@pytest.mark.usefixtures("valid_op_cli_config_xdg_config_op_account_2")
def test_op_cli_config_two_valid_03(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config in ~/.config/op location (rule 5) with example-account data
        AND a valid op config in ${XDG_CONFIG_HOME}/op location (rule 6) with example-account-2 data

    Create:
        OPCLIConfig object

    Verify:
        The config from rule 5 (~/.config/op) is found and used before the config from rule 6
        Tests config search order priority when both configs are valid
        Verifies the higher priority config (example-account) is loaded
    """
    expected = expected_op_config_data.data_for_key("example-account")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand")
    assert result.shorthand == expected.shorthand
    assert result.account_uuid == expected.account_uuid
    assert result.email == expected.email
    assert result.url == expected.url


@pytest.mark.usefixtures("valid_op_cli_config_homedir_account_2")
@pytest.mark.usefixtures("valid_op_cli_config_xdg_config_op")
def test_op_cli_config_two_valid_04(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config in ~/.op location (rule 3) with example-account-2 data
        AND a valid op config in ${XDG_CONFIG_HOME}/op location (rule 6) with example-account data

    Create:
        OPCLIConfig object

    Verify:
        The config from rule 3 (~/.op) is found and used before the config from rule 6
        Tests config search order priority when both configs are valid
        Verifies the higher priority config (example-account-2) is loaded
    """
    expected = expected_op_config_data.data_for_key("example-account-2")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand_2")
    assert result.shorthand == expected.shorthand
    assert result.account_uuid == expected.account_uuid
    assert result.email == expected.email
    assert result.url == expected.url


@pytest.mark.usefixtures("valid_op_cli_config_xdghome_account_2")
@pytest.mark.usefixtures("valid_op_cli_config_home_config_op")
def test_op_cli_config_two_valid_05(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config in ${XDG_CONFIG_HOME}/.op location (rule 4) with example-account-2 data
        AND a valid op config in ~/.config/op location (rule 5) with example-account data

    Create:
        OPCLIConfig object

    Verify:
        The config from rule 4 (${XDG_CONFIG_HOME}/.op) is found and used before the config from rule 5
        Tests config search order priority when both configs are valid
        Verifies the higher priority config (example-account-2) is loaded
    """
    expected = expected_op_config_data.data_for_key("example-account-2")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand_2")
    assert result.shorthand == expected.shorthand
    assert result.account_uuid == expected.account_uuid
    assert result.email == expected.email
    assert result.url == expected.url


@pytest.mark.usefixtures("valid_op_cli_config_op_config_dir_account_2")
@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_op_cli_config_two_valid_06(expected_op_config_data: ExpectedConfigData, console_logger):
    """
    Stage:
        A valid op config via OP_CONFIG_DIR (rule 2) with example-account-2 data
        AND a valid op config in ~/.op location (rule 3) with example-account data

    Create:
        OPCLIConfig object

    Verify:
        The config from rule 2 (OP_CONFIG_DIR) is found and used before the config from rule 3
        Tests config search order priority when both configs are valid
        Verifies the higher priority config (example-account-2) is loaded
    """
    expected = expected_op_config_data.data_for_key("example-account-2")
    config = OPCLIConfig(logger=console_logger)
    result = config.get_config("example_shorthand_2")
    assert result.shorthand == expected.shorthand
    assert result.account_uuid == expected.account_uuid
    assert result.email == expected.email
    assert result.url == expected.url


# ERROR CONDITION TESTS

@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_op_cli_config_homedir_07():
    """
    Stage:
        A valid op config in the default location under "$HOME" (rule 3)

    Create:
        OPCLIConfig object with default parameters

    Verify:
        Calling get_config() with a non-existent shorthand raises OPConfigNotFoundException
    """
    _sanity_check_standard_home_env()
    shorthand = "NO_SUCH_SHORTHAND"
    config = OPCLIConfig()
    with pytest.raises(OPConfigNotFoundException):
        config.get_config(shorthand)


@pytest.mark.usefixtures("expected_op_config_data", "valid_op_cli_config_xdghome")
def test_op_cli_config_xdg_07(console_logger):
    """
    Stage:
        A valid op config in ${XDG_CONFIG_HOME}/.op location (rule 4)
        XDG_CONFIG_HOME is set, HOME is set to /dev/null

    Create:
        OPCLIConfig object

    Verify:
        Calling get_config() with a non-existent shorthand raises OPConfigNotFoundException
    """
    shorthand = "NO_SUCH_SHORTHAND"
    config = OPCLIConfig(logger=console_logger)
    with pytest.raises(OPConfigNotFoundException):
        config.get_config(shorthand)


@pytest.mark.usefixtures("invalid_op_cli_config_unreable")
def test_op_cli_config_unreable_01(console_logger):
    """
    Stage:
        An unreadable op config file (no read permissions) in ~/.op location (rule 3)

    Create:
        OPCLIConfig object

    Verify:
        OPConfigNotFoundException is raised when config file cannot be read
        (Note: This test will fail if run as root, as root can read any file)
    """
    # NOTE: This test will fail if run as root (e.g., in a docker container with no users)
    # there is no way to make a file unreadable to root
    if not is_windows():
        # this test depends on creating a config file that's not readable
        # this is not straightforward on windows via native python APIs
        # so only run this test if not on windows
        with pytest.raises(OPConfigNotFoundException):
            OPCLIConfig(logger=console_logger)
    else:
        assert True


@pytest.mark.usefixtures("invalid_op_cli_config_missing")
def test_op_cli_config_missing_01(console_logger):
    """
    Stage:
        A missing op config file (file deleted after creation)

    Create:
        OPCLIConfig object with default parameters

    Verify:
        OPConfigNotFoundException is raised when config file is missing
    """
    with pytest.raises(OPConfigNotFoundException):
        OPCLIConfig(logger=console_logger)


@pytest.mark.usefixtures("invalid_op_cli_config_missing")
def test_op_cli_config_missing_02(console_logger):
    """
    Stage:
        A missing op config file (file deleted after creation)

    Create:
        OPCLIConfig object with explicit non-existent config_dir

    Verify:
        OPConfigNotFoundException is raised when specified config directory doesn't exist
    """
    with pytest.raises(OPConfigNotFoundException):
        OPCLIConfig(config_dir="no_such_path", logger=console_logger)


@pytest.mark.usefixtures("invalid_op_cli_config_malformed")
def test_op_cli_config_malformed_01(console_logger):
    """
    Stage:
        A malformed op config file (invalid JSON) in ~/.op location (rule 3)

    Create:
        OPCLIConfig object

    Verify:
        OPConfigNotFoundException is raised when config file contains invalid JSON
    """
    with pytest.raises(OPConfigNotFoundException):
        OPCLIConfig(logger=console_logger)


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
def test_op_cli_config_missing_shorthand_01(console_logger):
    """
    Stage:
        A valid op config with empty 'latest_signin' shorthand in ~/.op location (rule 3)

    Create:
        OPCLIConfig object

    Verify:
        OPConfigNotFoundException is raised when calling get_config() with no arguments
        and latest_signin shorthand is empty
    """
    conf = OPCLIConfig(logger=console_logger)
    with pytest.raises(OPConfigNotFoundException):
        conf.get_config()


# EDGE CASES

@pytest.mark.usefixtures("valid_op_cli_config_no_account_list")
# @pytest.mark.usefixtures("setup_normal_op_env")
def test_op_cli_config_no_account_list_01():
    """
    Verify we can instantiate OPCLIConfig() even when account list is null
    """
    OPCLIConfig()
