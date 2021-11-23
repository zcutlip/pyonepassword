import datetime
from typing import Dict

from ..test_support._datetime import fromisoformat_z
from .expected_data import ExpectedData


class ExpectedItemPassword:
    def __init__(self, user_dict: Dict):
        self._data = user_dict

    @property
    def password(self) -> str:
        return self._data["password"]

    @property
    def uuid(self) -> str:
        return self._data["uuid"]

    @property
    def title(self) -> str:
        return self._data["title"]

    @property
    def created_at(self) -> datetime.datetime:
        created_at = self._data["createdAt"]
        return fromisoformat_z(created_at)

    @property
    def updated_at(self) -> datetime.datetime:
        updated_at = self._data["updatedAt"]
        return fromisoformat_z(updated_at)

    @property
    def changer_uuid(self) -> str:
        return self._data["changerUuid"]

    @property
    def vault_uuid(self) -> str:
        return self._data["vaultUuid"]

    @property
    def trashed(self) -> bool:
        return self._data["trashed"]

    @property
    def returncode(self) -> int:
        return self._data["returncode"]


class ExpectedItemPasswordData:
    def __init__(self):
        expected_data = ExpectedData()
        item_data: Dict = expected_data.item_data
        self._data: Dict = item_data

    def data_for_password(self, password_identifier: str):
        item_dict = self._data[password_identifier]
        password_item = ExpectedItemPassword(item_dict)
        return password_item
