import datetime

from typing import Dict, List

from ..test_support._datetime import fromisoformat_z
from .expected_data import ExpectedData


class ExpectedGroup:
    def __init__(self, group_dict: Dict):
        self._data = group_dict

    @property
    def unique_id(self) -> str:
        return self._data["unique_id"]

    @property
    def description(self) -> str:
        return self._data["description"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def created_at(self) -> datetime.datetime:
        created_at = self._data["created_at"]
        return fromisoformat_z(created_at)

    @property
    def updated_at(self) -> datetime.datetime:
        updated_at = self._data["updated_at"]
        return fromisoformat_z(updated_at)

    @property
    def returncode(self) -> int:
        return self._data["returncode"]

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def state(self) -> str:
        return self._data["state"]

    @property
    def permissions(self) -> List[str]:
        return self._data["permissions"]


class ExpectedGroupData:
    def __init__(self):
        expected_data = ExpectedData()
        group_data: Dict = expected_data.group_data
        self._data: Dict = group_data

    def data_for_group(self, group_identifier: str):
        group_dict = self._data[group_identifier]
        group = ExpectedGroup(group_dict)
        return group


class ExpectedGroupListEntry:
    def __init__(self, user_item: Dict) -> None:
        self._data = user_item

    @property
    def unique_id(self) -> str:
        return self._data["unique_id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def description(self) -> str:
        return self._data["description"]

    @property
    def state(self) -> str:
        return self._data["state"]

    @property
    def created_at(self) -> datetime.datetime:
        created = self._data["created_at"]
        created = fromisoformat_z(created)
        return created


class ExpectedGroupListData:

    def __init__(self) -> None:
        expected_data = ExpectedData()
        group_list_data: Dict = expected_data.group_list_data
        self._data: Dict = group_list_data

    def data_for_key(self, data_key: str):
        group_list = self._data[data_key]
        group_list = [ExpectedGroupListEntry(entry_dict)
                      for entry_dict in group_list]
        return group_list
