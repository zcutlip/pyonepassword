import datetime
from typing import Dict

from .expected_data import ExpectedData
from ..test_support._datetime import fromisoformat_z


class ExpectedItemBase:
    def __init__(self, item_dict: Dict):
        self._data = item_dict

    @property
    def password(self) -> str:
        return self._data["password"]

    @property
    def unique_id(self) -> str:
        return self._data["unique_id"]

    @property
    def title(self) -> str:
        return self._data["title"]

    @property
    def created_at(self) -> datetime.datetime:
        created_at = self._data["created_at"]
        return fromisoformat_z(created_at)

    @property
    def updated_at(self) -> datetime.datetime:
        updated_at = self._data["updated_at"]
        return fromisoformat_z(updated_at)

    @property
    def last_edited_by(self) -> str:
        return self._data["last_edited_by"]

    @property
    def vault_id(self) -> str:
        return self._data["vaultUuid"]

    @property
    def returncode(self) -> int:
        return self._data["returncode"]


class ExpectedItemData:
    def __init__(self):
        expected_data = ExpectedData()
        item_data: Dict = expected_data.item_data
        self._data: Dict = item_data
