import os

from pytest import fixture

from pyonepassword import OP
from pyonepassword.py_op_exceptions import OPCmdFailedException

from .expected_account_data import ExpectedAccountData
from .expected_api_credential_data import ExpectedAPICredentialData
from .expected_credit_card import ExpectedCreditCardData
from .expected_data import ExpectedData
from .expected_datetimes import ExpectedDatetimeData
from .expected_document_data import ExpectedDocumentData
from .expected_group_data import ExpectedGroupData, ExpectedGroupListData
from .expected_item_fields import ExpectedItemFieldData
from .expected_login import ExpectedLoginItemData
from .expected_op_cli_config import ExpectedConfigData
from .expected_password_item_data import ExpectedPasswordItemData
from .expected_secure_note_item_data import ExpectedSecureNoteItemData
from .expected_server import ExpectedServerItemData
from .expected_totp_data import ExpectedTOTPData
from .expected_user_data import ExpectedUserData, ExpectedUserListData
from .expected_vault_data import ExpectedVaultData, ExpectedVaultListData
from .invalid_data import InvalidData
from .invalid_op_cli_config import (
    MalformedOPCLIConfig,
    MissingOPCLIConfig,
    UnreadableOPCLIConfig
)
from .paths import ALT_RESP_DIRECTORY_PATH, RESP_DIRECTORY_PATH
from .valid_data import ValidData
from .valid_op_cli_config import (
    VALID_OP_CONFIG_NO_SHORTHAND_KEY,
    ValidOPCLIConfig
)

TEST_DATA_VAULT = "Test Data"
OP_MASTER_PASSWORD = "made-up-password"
ACCOUNT_SHORTHAND = "onepassword_username"


def _setup_normal_env():
    os.environ["MOCK_OP_RESPONSE_DIRECTORY"] = str(RESP_DIRECTORY_PATH)
    os.environ["MOCK_OP_SIGNIN_SUCCEED"] = "1"
    # os.environ["MOCK_OP_SIGNIN_USES_BIO"] = "1"
    os.environ["LOG_OP_ERR"] = "1"


def _setup_alt_env():
    os.environ["MOCK_OP_RESPONSE_DIRECTORY"] = str(ALT_RESP_DIRECTORY_PATH)
    os.environ["MOCK_OP_SIGNIN_SUCCEED"] = "1"
    # os.environ["MOCK_OP_SIGNIN_USES_BIO"] = "1"
    os.environ["LOG_OP_ERR"] = "1"


def _get_signed_in_op(account_shorthand, default_vault=None):
    _setup_normal_env()
    try:
        op = OP(vault=default_vault, account_shorthand=account_shorthand,
                password=OP_MASTER_PASSWORD, op_path='mock-op')
    except OPCmdFailedException as e:
        print(f"OP() failed: {e.err_output}")
        raise e
    return op


@fixture
def setup_normal_op_env():
    _setup_normal_env()


@fixture
def setup_alt_op_env():
    _setup_alt_env()


@fixture
def signed_in_op():
    op = _get_signed_in_op(ACCOUNT_SHORTHAND)
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
def expected_datetime_data():
    data = ExpectedDatetimeData()
    return data


@fixture
def expected_op_config_data():
    data = ExpectedConfigData()
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
