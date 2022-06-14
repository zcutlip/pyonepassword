from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP
    from pyonepassword.api.object_types import OPCreditCardItem

    from .fixtures.expected_credit_card import ExpectedCreditCardData


pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_item_getcredit_card_01(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.credit_card_number == expected.credit_card_number


def test_item_getcredit_card_02(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.cvv == expected.cvv


def test_item_getcredit_card_03(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.expiry_date == expected.expiry_date


def test_item_getcredit_card_04(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.valid_from == expected.valid_from


def test_item_getcredit_card_05(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.pin == expected.pin


def test_item_getcredit_card_06(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.credit_limit == expected.credit_limit


def test_item_getcredit_card_07(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.cash_withdrawal_limit == expected.cash_withdrawal_limit


def test_item_getcredit_card_08(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.interest_rate == expected.interest_rate


def test_item_getcredit_card_09(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.unique_id == expected.unique_id


def test_item_getcredit_card_10(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.title == expected.title


def test_item_getcredit_card_11(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.created_at == expected.created_at


def test_item_getcredit_card_12(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.updated_at == expected.updated_at


def test_item_getcredit_card_13(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.last_edited_by == expected.last_edited_by


def test_item_getcredit_card_14(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.item_get(
        credit_card_id, vault=vault)

    assert result.issue_number == expected.issue_number
