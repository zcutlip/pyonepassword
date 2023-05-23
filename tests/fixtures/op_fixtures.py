import os
import shutil
import tempfile
from pathlib import Path

from pytest import fixture

from pyonepassword import OP, logging
from pyonepassword.api.exceptions import OPCmdFailedException

from .expected_account_data import ExpectedAccountData
from .expected_api_credential_data import ExpectedAPICredentialData
from .expected_credit_card import ExpectedCreditCardData
from .expected_data import ExpectedData
from .expected_database import ExpectedDatabaseItemData
from .expected_datetimes import ExpectedDatetimeData
from .expected_document_data import ExpectedDocumentData
from .expected_group_data import ExpectedGroupData, ExpectedGroupListData
from .expected_identity import ExpectedIdenityItemData
from .expected_item import ExpectedItemData
from .expected_item_fields import ExpectedItemFieldData
from .expected_item_list import ExpectedItemListData
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
from .non_comformant_data import NonConformantData
from .paths import (
    ALT_RESP_DIRECTORY_PATH,
    ITEM_DELETE_MULTIPLE_STATE_CONFIG_PATH,
    ITEM_DELETE_MULTIPLE_TITLE_GLOB_STATE_CONFIG_PATH,
    RESP_DIRECTORY_PATH,
    SVC_ACCT_CORRUPT_RESP_DIRECTORY_PATH,
    SVC_ACCT_RESP_DIRECTORY_PATH,
    UNAUTH_RESP_DIRECTORY_PATH
)
from .platform_support import HOME_ENV_VAR
from .valid_data import ValidData
from .valid_op_cli_config import (
    VALID_OP_CONFIG_NO_ACCOUNT_LIST_KEY,
    VALID_OP_CONFIG_NO_SHORTHAND_KEY,
    ValidOPCLIConfig
)

TEST_DATA_VAULT = "Test Data"
OP_MASTER_PASSWORD = "made-up-password"
ACCOUNT_ID = "5GHHPJK5HZC5BAT7WDUXW57G44"

# set up console logger early, because pytest comes behind and messes with sys.stderr/sys.stdout
# otherwise anomolies happen like duplicated log messages, etc.
op_console_logger = logging.console_logger("pytest", logging.DEBUG)


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
    old_home = os.environ.get(HOME_ENV_VAR)
    # keep handle to temp_dir so it doesn't get auto-cleaned before we're done with it
    # because we yield below rather than return, it should stay in scope
    temp_dir = tempfile.TemporaryDirectory()
    tmp_home = temp_dir.name
    os.environ[HOME_ENV_VAR] = tmp_home
    yield
    os.environ.pop(HOME_ENV_VAR, None)
    if old_home is not None:
        # only restore HOME env variable if it was set to start with
        # in some minimal environments (e.g., some docker containers) there
        # is no $HOME env variable
        os.environ[HOME_ENV_VAR] = old_home


def _setup_normal_env(signin_success="1"):
    # don't set MOCK_OP_RESPONSE_DIRECTORY
    # if we're using MOCK_OP_STATE_DIR
    if not os.environ.get("MOCK_OP_STATE_DIR"):
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
    os.environ["MOCK_OP_SIGNIN_ACCOUNT"] = "5GHHPJK5HZC5BAT7WDUXW57G44"


def _setup_no_bio_alt_env():
    _setup_alt_env()
    os.environ["MOCK_OP_SIGNIN_USES_BIO"] = "0"
    os.environ["MOCK_OP_SIGNIN_ACCOUNT"] = "5GHHPJK5HZC5BAT7WDUXW57G44"


def _setup_unauth_env():
    os.environ["MOCK_OP_RESPONSE_DIRECTORY"] = str(UNAUTH_RESP_DIRECTORY_PATH)
    os.environ["MOCK_OP_SIGNIN_SUCCEED"] = "1"
    # os.environ["MOCK_OP_SIGNIN_USES_BIO"] = "1"
    os.environ["LOG_OP_ERR"] = "1"


def _setup_svc_acct_env():
    svc_account_token = os.environ["PYTEST_SVC_ACCT_TOKEN"]
    os.environ["OP_SERVICE_ACCOUNT_TOKEN"] = svc_account_token
    # don't set MOCK_OP_RESPONSE_DIRECTORY
    # if we're using MOCK_OP_STATE_DIR
    if not os.environ.get("MOCK_OP_STATE_DIR"):
        os.environ["MOCK_OP_RESPONSE_DIRECTORY"] = str(
            SVC_ACCT_RESP_DIRECTORY_PATH)

    os.environ["MOCK_OP_SIGNIN_SUCCEED"] = "1"
    os.environ["LOG_OP_ERR"] = "1"


def _setup_svc_acct_corrupt_env():
    svc_account_token = os.environ["PYTEST_SVC_ACCT_TOKEN"]
    os.environ["OP_SERVICE_ACCOUNT_TOKEN"] = svc_account_token
    # don't set MOCK_OP_RESPONSE_DIRECTORY
    # if we're using MOCK_OP_STATE_DIR
    if not os.environ.get("MOCK_OP_STATE_DIR"):
        os.environ["MOCK_OP_RESPONSE_DIRECTORY"] = str(
            SVC_ACCT_CORRUPT_RESP_DIRECTORY_PATH)

    os.environ["MOCK_OP_SIGNIN_SUCCEED"] = "1"
    os.environ["LOG_OP_ERR"] = "1"


@fixture
def setup_stateful_item_delete_multiple():

    # set up a temporary directory to copy the state config to, since it gets modified
    # during state iteration
    temp_dir = tempfile.TemporaryDirectory()
    state_config_dir = temp_dir.name
    state_config_path = Path(state_config_dir, "config.json")
    shutil.copyfile(ITEM_DELETE_MULTIPLE_STATE_CONFIG_PATH, state_config_path)

    # now pop MOCK_OP_RESPONSE_DIRECTORY to ensure it doesn't conflict with with
    # the stateful config
    old_mock_op_resp_dir = os.environ.pop("MOCK_OP_RESPONSE_DIRECTORY", None)
    os.environ["MOCK_OP_STATE_DIR"] = state_config_dir
    yield  # pytest will return us here after the test runs
    # get rid of MOCK_OP_STATE_DIR
    os.environ.pop("MOCK_OP_STATE_DIR")

    # restore MOCK_OP_RESPONSE_DIRECTORY if it was previously set
    if old_mock_op_resp_dir is not None:
        os.environ["MOCK_OP_RESPONSE_DIRECTORY"] = old_mock_op_resp_dir

    # temp_dir will get cleaned up once we return


@fixture
def setup_stateful_item_delete_multiple_title_glob():

    # set up a temporary directory to copy the state config to, since it gets modified
    # during state iteration
    temp_dir = tempfile.TemporaryDirectory()
    state_config_dir = temp_dir.name
    state_config_path = Path(state_config_dir, "config.json")
    shutil.copyfile(
        ITEM_DELETE_MULTIPLE_TITLE_GLOB_STATE_CONFIG_PATH, state_config_path)

    # now pop MOCK_OP_RESPONSE_DIRECTORY to ensure it doesn't conflict with with
    # the stateful config
    old_mock_op_resp_dir = os.environ.pop("MOCK_OP_RESPONSE_DIRECTORY", None)
    os.environ["MOCK_OP_STATE_DIR"] = state_config_dir
    yield  # pytest will return us here after the test runs
    # get rid of MOCK_OP_STATE_DIR
    os.environ.pop("MOCK_OP_STATE_DIR")

    # restore MOCK_OP_RESPONSE_DIRECTORY if it was previously set
    if old_mock_op_resp_dir is not None:
        os.environ["MOCK_OP_RESPONSE_DIRECTORY"] = old_mock_op_resp_dir

    # temp_dir will get cleaned up once we return


def _get_signed_in_op(account_id=None, default_vault=None, skip_env=False):
    # don't create a new console logger. use the module-level op_console_logger
    # to avoid problems with the way pytest captures sys.stderr/sys.stdout
    if not skip_env:
        _setup_normal_env()
    try:
        op = OP(vault=default_vault, account=account_id,
                password=OP_MASTER_PASSWORD, op_path='mock-op', logger=op_console_logger)
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
def setup_svc_acct_env():
    _setup_svc_acct_env()


@fixture
def setup_svc_acct_corrupt_env():
    _setup_svc_acct_corrupt_env()


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
    op = _get_signed_in_op(account_id=ACCOUNT_ID)
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
def expected_item_data():
    data = ExpectedItemData()
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
def expected_database_data():
    data = ExpectedDatabaseItemData()
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
def expected_item_list_data():
    data = ExpectedItemListData()
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
def non_conformant_data():
    data = NonConformantData()
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
    # don't create a new console logger. use the module-level op_console_logger
    # to avoid problems with the way pytest captures sys.stderr/sys.stdout
    return op_console_logger
