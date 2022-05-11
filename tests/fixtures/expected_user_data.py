import datetime

from typing import Dict, Union

from ..test_support._datetime import fromisoformat_z
from .expected_data import ExpectedData


class ExpectedUser:
    def __init__(self, user_dict: Dict):
        self._data = user_dict

    @property
    def unique_id(self) -> str:
        return self._data["unique_id"]

    @property
    def created_at(self) -> datetime.datetime:
        created_at = self._data["created_at"]
        return fromisoformat_z(created_at)

    @property
    def updated_at(self) -> datetime.datetime:
        updated_at = self._data["updated_at"]
        return fromisoformat_z(updated_at)

    @property
    def last_auth_at(self) -> datetime.datetime:
        updated_at = self._data["lastAuthAt"]
        return fromisoformat_z(updated_at)

    @property
    def email(self) -> str:
        return self._data["email"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def returncode(self) -> int:
        return self._data["returncode"]

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def state(self) -> str:
        return self._data["state"]


class ExpectedUserData:
    def __init__(self):
        expected_data = ExpectedData()
        user_data: Dict = expected_data.user_data
        self._data: Dict = user_data

    def data_for_user(self, user_identifier: str):
        user_dict = self._data[user_identifier]
        user = ExpectedUser(user_dict)
        return user


class ExpectedUserListEntry:
    def __init__(self, user_item: Dict) -> None:
        self._data = user_item

    @property
    def unique_id(self) -> str:
        return self._data["unique_id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def email(self) -> str:
        return self._data["email"]

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def state(self) -> str:
        return self._data["state"]

    @property
    def role(self) -> Union[str, None]:
        return self._data.get("role")


class ExpectedUserListData:

    def __init__(self) -> None:
        expected_data = ExpectedData()
        user_list_data: Dict = expected_data.user_list_data
        self._data: Dict = user_list_data

    def data_for_key(self, data_key: str):
        user_list = self._data[data_key]
        user_list = [ExpectedUserListEntry(entry_dict)
                     for entry_dict in user_list]
        return user_list
