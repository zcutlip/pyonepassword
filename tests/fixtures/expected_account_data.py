from typing import Dict

from .expected_data import ExpectedData


class ExpectedAccount:
    def __init__(self, account_dict):
        self._data = account_dict

    @property
    def account_uuid(self) -> str:
        return self._data["account_uuid"]

    @property
    def user_uuid(self) -> str:
        return self._data["user_uuid"]

    @property
    def url(self) -> str:
        return self._data["url"]

    @property
    def email(self) -> str:
        return self._data["email"]

    @property
    def shorthand(self) -> str:
        return self._data.get("shorthand")


class ExpectedAccountData:
    def __init__(self):
        expected_data = ExpectedData()
        account_data: Dict = expected_data.account_data
        self._data: Dict = account_data

    def data_for_account(self, account_identifier: str):
        account_dict = self._data[account_identifier]
        account = ExpectedAccount(account_dict)
        return account
