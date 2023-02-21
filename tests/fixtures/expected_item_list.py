import datetime
from typing import Dict, List

from ..test_support._datetime import fromisoformat_z
from .paths import (
    EXPECTED_ITEM_LIST_DATA_PATH,
    EXPECTED_ITEM_LIST_DATA_REGISTRY_PATH
)
from .valid_data import ValidData


class _ItemEntry:
    # {
    #     "id": "3gd3kpilkrhwc4yn6z6eca76ru",
    #     "title": "Example Login Item 02",
    #     "version": 1,
    #     "vault": {
    #         "id": "ptpmg6qseanbhoesdooqniehhy",
    #         "name": "Test Data 3"
    #     },
    #     "category": "LOGIN",
    #     "created_at": "2023-02-19T21:18:42.966131-08:00",
    #     "updated_at": "2023-02-19T21:18:42.966131-08:00",
    #     "additional_information": "user_02"
    # }

    def __init__(self, item_entry_dict) -> None:
        self._data = item_entry_dict

    @property
    def unique_id(self) -> str:
        return self._data["id"]

    @property
    def title(self) -> str:
        return self._data["title"]

    @property
    def category(self) -> str:
        return self._data["category"]

    @property
    def created_at(self) -> datetime.datetime:
        created_at = self._data["created_at"]
        return fromisoformat_z(created_at)

    @property
    def updated_at(self) -> datetime.datetime:
        updated_at = self._data["updated_at"]
        return fromisoformat_z(updated_at)

    @property
    def version(self) -> int:
        return self._data["version"]


class ExpectedItemList(List[_ItemEntry]):
    def __init__(self, expected_data: Dict):
        super().__init__()
        self._data = expected_data["meta"]
        items = expected_data["data"]
        for item_dict in items:
            item = _ItemEntry(item_dict)
            self.append(item)

        self.sort()

    def sort(self):
        super().sort(key=lambda item: item.unique_id)
        super().sort(key=lambda item: item.title)

    @property
    def returncode(self) -> int:
        return self._data["returncode"]


class ExpectedItemListData(ValidData):
    REGISTRY_PATH = EXPECTED_ITEM_LIST_DATA_REGISTRY_PATH
    DATA_PATH = EXPECTED_ITEM_LIST_DATA_PATH

    def data_for_name(self, entry_name) -> ExpectedItemList:
        data = super().data_for_name(entry_name)
        expected_data = ExpectedItemList(data)
        return expected_data
