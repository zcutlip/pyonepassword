from typing import Dict

from .expected_item import ExpectedItemBase
from .expected_data import ExpectedData


class ExpectedItemPassword(ExpectedItemBase):

    @property
    def password(self) -> str:
        return self._data["password"]


class ExpectedItemPasswordData:
    def __init__(self):
        expected_data = ExpectedData()
        item_data: Dict = expected_data.item_data
        self._data: Dict = item_data

    def data_for_password(self, password_identifier: str):
        item_dict = self._data[password_identifier]
        password_item = ExpectedItemPassword(item_dict)
        return password_item
