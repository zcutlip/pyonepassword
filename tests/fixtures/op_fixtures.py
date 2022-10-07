import os
import tempfile

from pytest import fixture

from pyonepassword import OP, logging
from pyonepassword.api.exceptions import OPCmdFailedException

from .expected_account_data import ExpectedAccountData
from .expected_api_credential_data import ExpectedAPICredentialData
from .expected_credit_card import ExpectedCreditCardData
from .expected_data import ExpectedData
from .expected_datetimes import ExpectedDatetimeData
from .expected_document_data import ExpectedDocumentData
from .expected_group_data import ExpectedGroupData, ExpectedGroupListData
from .expected_identity import ExpectedIdenityItemData
from .expected_item_fields import ExpectedItemFieldData
from .expected_item_sections import ExpectedItemSectionData
from .expected_login import ExpectedLoginItemData
from .expected_miscellaneous_data import ExpectedMiscData
from .expected_op_cli_config import ExpectedConfigData
from .expected_password_item_data import ExpectedPasswordItemData
from .expected_secure_note_item_data import ExpectedSecureNoteItemData
from .expected_server import ExpectedServerItemData
from .expected_ssh_key_data import ExpectedSSHKeyData
from .expected_totp_data import ExpectedTOTPData
from .expected_user_data import ExpectedUserData, ExpectedUserListData
from .expected_vault_data import ExpectedVaultData, ExpectedVaultListData
from .invalid_data import InvalidData
from .invalid_op_cli_config import (
    MalformedOPCLIConfig,
    MissingOPCLIConfig,
    UnreadableOPCLIConfig
)
from .paths import (
    ALT_RESP_DIRECTORY_PATH,
    RESP_DIRECTORY_PATH,
    UNAUTH_RESP_DIRECTORY_PATH
)
from .valid_data import ValidData
from .valid_op_cli_config import (
    VALID_OP_CONFIG_NO_ACCOUNT_LIST_KEY,
    VALID_OP_CONFIG_NO_SHORTHAND_KEY,
    ValidOPCLIConfig
)

TEST_DATA_VAULT = "Test Data"
OP_MASTER_PASSWORD = "made-up-password"
ACCOUNT_ID = "5GHHPJK5HZC5BAT7WDUXW57G44"


@fixture(autouse=True, scope='function')
def save_restore_env():
    """
    pyonepassword modifies os.environ
    before each test, we need to save a copy
    and after the test/before the next, restore the copy
    """
    orig_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(orig_env)


@fixture(autouse=True, scope="function")
def temp_home():
    """
    Ensure no test is inadvertantly relying on the real user's op config/home directory
    Set $HOME to an empty tmpdir
    If a test needs a valid op config/home directory, it should explicitly request
    one using a fixture
    """
    old_home = os.environ.get('HOME')
    tmp_home = tempfile.TemporaryDirectory().name
    os.environ['HOME'] = tmp_home
    yield
    os.environ.pop('HOME', None)
    if old_home is not None:
        # only restore HOME env variable if it was set to start with
        # in some minimal environments (e.g., some docker containers) there
        # is no $HOME env variable
        os.environ['HOME'] = old_home


def _setup_normal_env(signin_success="1"):
    os.environ["MOCK_OP_RESPONSE_DIRECTORY"] = str(RESP_DIRECTORY_PATH)
    os.environ["MOCK_OP_SIGNIN_SUCCEED"] = str(signin_success)
    # os.environ["MOCK_OP_SIGNIN_USES_BIO"] = "1"
    os.environ["LOG_OP_ERR"] = "1"


def _setup_alt_env():
    os.environ["MOCK_OP_RESPONSE_DIRECTORY"] = str(ALT_RESP_DIRECTORY_PATH)
    os.environ["MOCK_OP_SIGNIN_SUCCEED"] = "1"
    # os.environ["MOCK_OP_SIGNIN_USES_BIO"] = "1"
    os.environ["LOG_OP_ERR"] = "1"


def _setup_no_bio_normal_env():
    _setup_normal_env()
    os.environ["MOCK_OP_SIGNIN_USES_BIO"] = "0"
    os.environ["MOCK_OP_SIGNIN_SHORTHAND"] = "5GHHPJK5HZC5BAT7WDUXW57G44"


def _setup_no_bio_alt_env():
    _setup_alt_env()
    os.environ["MOCK_OP_SIGNIN_USES_BIO"] = "0"
    os.environ["MOCK_OP_SIGNIN_SHORTHAND"] = "5GHHPJK5HZC5BAT7WDUXW57G44"


def _setup_unauth_env():
    os.environ["MOCK_OP_RESPONSE_DIRECTORY"] = str(UNAUTH_RESP_DIRECTORY_PATH)
    os.environ["MOCK_OP_SIGNIN_SUCCEED"] = "1"
    # os.environ["MOCK_OP_SIGNIN_USES_BIO"] = "1"
    os.environ["LOG_OP_ERR"] = "1"


def _get_signed_in_op(account_id, default_vault=None):
    logger = logging.console_logger("pytest", logging.DEBUG)
    _setup_normal_env()
    try:
        op = OP(vault=default_vault, account=account_id,
                password=OP_MASTER_PASSWORD, op_path='mock-op', logger=logger)
    except OPCmdFailedException as e:
        print(f"OP() failed: {e.err_output}")
        raise e
    return op


@fixture
def setup_normal_op_env():
    _setup_normal_env()


@fixture
def setup_no_bio_normal_op_env():
    _setup_no_bio_normal_env()


@fixture
def setup_normal_op_env_signin_failure():
    _setup_normal_env(signin_success="0")


@fixture
def setup_alt_op_env():
    _setup_alt_env()


@fixture
def setup_no_bio_alt_op_env():
    _setup_no_bio_alt_env()


@fixture
def setup_unauth_op_env():
    _setup_unauth_env()


@fixture
def setup_op_sess_var_alt_env(setup_alt_op_env):
    misc_data = ExpectedMiscData()
    sess_var_name = misc_data.data_for_key("op-session-var")
    sess_token = misc_data.data_for_key("op-session-token")
    os.environ[sess_var_name] = sess_token


@fixture
def setup_op_sess_var_unauth_env(setup_unauth_op_env):
    misc_data = ExpectedMiscData()
    sess_var_name = misc_data.data_for_key("op-session-var")
    sess_token = misc_data.data_for_key("op-session-token")
    os.environ[sess_var_name] = sess_token


@fixture
def signed_in_op():
    op = _get_signed_in_op(ACCOUNT_ID)
    return op


@fixture
def expected_data():
    data = ExpectedData()
    return data


@fixture
def expected_user_data():
    data = ExpectedUserData()
    return data


@fixture
def expected_user_list_data():
    data = ExpectedUserListData()
    return data


@fixture
def expected_vault_data():
    data = ExpectedVaultData()
    return data


@fixture
def expected_vault_list_data():
    data = ExpectedVaultListData()
    return data


@fixture
def expected_group_data():
    data = ExpectedGroupData()
    return data


@fixture
def expected_group_list_data():
    data = ExpectedGroupListData()
    return data


@fixture
def expected_item_password_data():
    data = ExpectedPasswordItemData()
    return data


@fixture
def expected_secure_note_item_data():
    data = ExpectedSecureNoteItemData()
    return data


@fixture
def expected_document_data():
    data = ExpectedDocumentData()
    return data


@fixture
def expected_server_data():
    data = ExpectedServerItemData()
    return data


@fixture
def expected_credit_card_data():
    data = ExpectedCreditCardData()
    return data


@fixture
def expected_login_item_data():
    data = ExpectedLoginItemData()
    return data


@fixture
def expected_account_data():
    data = ExpectedAccountData()
    return data


@fixture
def expected_totp_data():
    data = ExpectedTOTPData()
    return data


@fixture
def expected_api_credential_data():
    data = ExpectedAPICredentialData()
    return data


@fixture
def expected_item_field_data():
    data = ExpectedItemFieldData()
    return data


@fixture
def expected_item_section_data():
    data = ExpectedItemSectionData()
    return data


@fixture
def expected_datetime_data():
    data = ExpectedDatetimeData()
    return data


@fixture
def expected_op_config_data():
    data = ExpectedConfigData()
    return data


@fixture
def expected_misc_data():
    data = ExpectedMiscData()
    return data


@fixture
def expected_ssh_key_data():
    data = ExpectedSSHKeyData()
    return data


@fixture
def expected_identity_data():
    data = ExpectedIdenityItemData()
    return data


@fixture
def invalid_data():
    data = InvalidData()
    return data


@fixture
def valid_data():
    data = ValidData()
    return data


@fixture
def valid_op_cli_config_homedir():
    config_obj = ValidOPCLIConfig()
    return config_obj


@fixture
def valid_op_cli_config_xdghome():
    config_obj = ValidOPCLIConfig(location_env_var='XDG_CONFIG_HOME')
    return config_obj


@fixture
def valid_op_cli_config_no_shorthand():
    config_obj = ValidOPCLIConfig(
        valid_data_key=VALID_OP_CONFIG_NO_SHORTHAND_KEY)
    return config_obj


@fixture
def valid_op_cli_config_no_account_list():
    """
    Stage an 'op' config that is perfectly valid but "accounts" == null
    """
    config_obj = ValidOPCLIConfig(
        valid_data_key=VALID_OP_CONFIG_NO_ACCOUNT_LIST_KEY)
    return config_obj


@fixture
def invalid_op_cli_config_unreable():
    config_obj = UnreadableOPCLIConfig()
    return config_obj


@fixture
def invalid_op_cli_config_missing():
    config_obj = MissingOPCLIConfig()
    return config_obj


@fixture
def invalid_op_cli_config_malformed():
    config_obj = MalformedOPCLIConfig()
    return config_obj


@fixture
def console_logger():
    logger = logging.console_logger("pytest", logging.DEBUG)
    return logger
