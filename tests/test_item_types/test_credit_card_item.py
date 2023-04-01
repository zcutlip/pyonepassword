from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..fixtures.expected_credit_card import ExpectedCreditCardData
    from ..fixtures.valid_data import ValidData

from pyonepassword.api.object_types import OPCreditCardItem


def test_credit_card_item_010(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - credit_card_number property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")

    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.credit_card_number == expected.credit_card_number


def test_credit_card_item_020(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - cvv property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.cvv == expected.cvv


def test_credit_card_item_030(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - expiry_date matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.expiry_date == expected.expiry_date


def test_credit_card_item_040(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - valid_from property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.valid_from == expected.valid_from


def test_credit_card_item_050(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - pin property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.pin == expected.pin


def test_credit_card_item_060(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - credit_limit property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.credit_limit == expected.credit_limit


def test_credit_card_item_070(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - cash_withdrawal_limit property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.cash_withdrawal_limit == expected.cash_withdrawal_limit


def test_credit_card_item_080(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - interest_rate property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.interest_rate == expected.interest_rate


def test_credit_card_item_090(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - unique_id property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.unique_id == expected.unique_id


def test_credit_card_item_100(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - title property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.title == expected.title


def test_credit_card_item_110(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - created_at property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.created_at == expected.created_at


def test_credit_card_item_120(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - updated_at property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.updated_at == expected.updated_at


def test_credit_card_item_130(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - last_edited_by property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.last_edited_by == expected.last_edited_by


def test_credit_card_item_140(valid_data: ValidData,
                              expected_credit_card_data: ExpectedCreditCardData):
    """
    Create:
        - credit card item object from "example credit card"
    Verify:
        - issue_number property matches expected value
    """
    credit_card_id = "Example Credit Card"
    item_dict = valid_data.data_for_name("example-credit-card")
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result = OPCreditCardItem(item_dict)

    assert result.issue_number == expected.issue_number
