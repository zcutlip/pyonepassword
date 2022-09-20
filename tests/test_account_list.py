from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.object_types import OPAccount

if TYPE_CHECKING:
    from pyonepassword import OP

    from .fixtures.expected_account_data import ExpectedAccountData


pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_account_list_01(signed_in_op: OP, expected_account_data: ExpectedAccountData):
    account_id = "user1@yahoo.com"
    account_list = signed_in_op.signed_in_accounts()
    account: OPAccount = account_list.account_for_identifier(account_id)
    assert isinstance(account, OPAccount)


def test_account_list_02(signed_in_op: OP, expected_account_data: ExpectedAccountData):
    account_id = "user1@yahoo.com"
    expected = expected_account_data.data_for_account(account_id)

    account_list = signed_in_op.signed_in_accounts()
    account: OPAccount = account_list.account_for_identifier(account_id)

    assert account.user_uuid == expected.user_uuid


def test_account_list_03(signed_in_op: OP, expected_account_data: ExpectedAccountData):
    account_id = "user2@yahoo.com"
    expected = expected_account_data.data_for_account(account_id)

    account_list = signed_in_op.signed_in_accounts()
    account: OPAccount = account_list.account_for_identifier(account_id)

    assert account.email == expected.email


def test_account_list_04(signed_in_op: OP, expected_account_data: ExpectedAccountData):
    account_id = "user2@yahoo.com"
    expected = expected_account_data.data_for_account(account_id)

    account_list = signed_in_op.signed_in_accounts()
    account: OPAccount = account_list.account_for_identifier(account_id)

    assert account.account_uuid == expected.account_uuid


def test_account_list_05(signed_in_op: OP, expected_account_data: ExpectedAccountData):
    account_id = "user1@yahoo.com"
    expected = expected_account_data.data_for_account(account_id)

    account_list = signed_in_op.signed_in_accounts()
    account: OPAccount = account_list.account_for_identifier(account_id)

    assert account.url == expected.url
