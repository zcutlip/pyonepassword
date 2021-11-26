from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pyonepassword import OP, OPCreditCardItem
    from .fixtures.expected_credit_card import ExpectedCreditCardData


def test_get_item_password_01(signed_in_op: OP, expected_credit_card_data: ExpectedCreditCardData):
    credit_card_id = "Example Credit Card"
    vault = "Test Data"
    expected = expected_credit_card_data.data_for_credit_card(credit_card_id)
    result: OPCreditCardItem = signed_in_op.get_item(
        credit_card_id, vault=vault)

    assert result.credit_card_number == expected.credit_card_number
    assert result.cvv == expected.cvv
    assert result.expiry_date == expected.expiry_date
    assert result.valid_from == expected.valid_from
    assert result.pin == expected.pin
    assert result.credit_limit == expected.credit_limit
    assert result.cash_withdrawal_limit == expected.cash_withdrawal_limit
    assert result.interest_rate == expected.interest_rate
    assert result.uuid == expected.uuid
    assert result.title == expected.title
    assert result.created_at == expected.created_at
    assert result.updated_at == expected.updated_at
    assert result.changer_uuid == expected.changer_uuid
    assert result.vault_uuid == expected.vault_uuid
    assert result.trashed == expected.trashed
