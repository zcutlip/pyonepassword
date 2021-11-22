import datetime

from typing import Dict

from ..test_support._datetime import fromisoformat_z
from .expected_data import ExpectedData


class ExpectedGroup:
    def __init__(self, group_dict: Dict):
        self._data = group_dict

    @property
    def uuid(self) -> str:
        return self._data["uuid"]

    @property
    def desc(self) -> str:
        return self._data["desc"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def created_at(self) -> datetime.datetime:
        created_at = self._data["createdAt"]
        return fromisoformat_z(created_at)

    @property
    def updated_at(self) -> datetime.datetime:
        updated_at = self._data["updatedAt"]
        return fromisoformat_z(updated_at)

    @property
    def returncode(self) -> int:
        return self._data["returncode"]


class ExpectedGroupData:
    def __init__(self):
        expected_data = ExpectedData()
        group_data: Dict = expected_data.group_data
        self._data: Dict = group_data

    def data_for_group(self, group_identifier: str):
        group_dict = self._data[group_identifier]
        group = ExpectedGroup(group_dict)
        return group
