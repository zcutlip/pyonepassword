from .expected_item import ExpectedItemBase, ExpectedItemData


class ExpectedCreditCard(ExpectedItemBase):
    """
    "Example Credit Card":{
            "credit_card_number": "3123456789012345",
            "cvv": "1234",
            "expiry_date": 204202,
            "valid_from": 198001,
            "pin": "9876",
            "credit_limit": "50000",
            "cash_withdrawal_limit": "3000",
            "interest_rate": "8%",
            "returncode": 0
        }
    """
    @property
    def credit_card_number(self) -> str:
        return self._data["credit_card_number"]

    @property
    def cvv(self) -> str:
        return self._data["cvv"]

    @property
    def expiry_date(self) -> int:
        return self._data["expiry_date"]

    @property
    def valid_from(self) -> int:
        return self._data["valid_from"]

    @property
    def pin(self) -> str:
        return self._data["pin"]

    @property
    def credit_limit(self) -> str:
        return self._data["credit_limit"]

    @property
    def cash_withdrawal_limit(self) -> str:
        return self._data["cash_withdrawal_limit"]

    @property
    def interest_rate(self) -> str:
        return self._data["interest_rate"]

    @property
    def issue_number(self) -> str:
        return self._data["issue_number"]


class ExpectedCreditCardData(ExpectedItemData):

    def data_for_credit_card(self, credit_card_identifier):
        item_dict = self.data_for_name(credit_card_identifier)
        note_item = ExpectedCreditCard(item_dict)
        return note_item
