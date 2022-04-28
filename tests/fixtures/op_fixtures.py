import os
from pytest import fixture
from pyonepassword import OP
from pyonepassword.py_op_exceptions import OPCmdFailedException

from .expected_data import ExpectedData
from .expected_credit_card import ExpectedCreditCardData
from .expected_document_data import ExpectedDocumentData
from .expected_group_data import ExpectedGroupData
from .expected_password_item_data import ExpectedPasswordItemData
from .expected_secure_note_item_data import ExpectedSecureNoteItemData
from .expected_server import ExpectedServerItemData
from .expected_user_data import ExpectedUserData
from .expected_vault_data import ExpectedVaultData
from .paths import RESP_DIRECTORY_PATH

TEST_DATA_VAULT = "Test Data"
OP_MASTER_PASSWORD = "made-up-password"
ACCOUNT_SHORTHAND = "onepassword_username"


def _get_signed_in_op(account_shorthand, default_vault=None):
    os.environ["MOCK_OP_RESPONSE_DIRECTORY"] = str(RESP_DIRECTORY_PATH)
    os.environ["MOCK_OP_SIGNIN_SUCCEED"] = "1"
    os.environ["MOCK_OP_SIGNIN_USES_BIO"] = "1"
    os.environ["LOG_OP_ERR"] = "1"
    try:
        op = OP(vault=default_vault, account_shorthand=account_shorthand,
                password=OP_MASTER_PASSWORD, op_path='mock-op')
    except OPCmdFailedException as e:
        print(f"OP() failed: {e.err_output}")
        raise e
    return op


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
def expected_vault_data():
    data = ExpectedVaultData()
    return data


@fixture
def expected_group_data():
    data = ExpectedGroupData()
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
