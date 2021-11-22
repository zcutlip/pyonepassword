import json
import datetime

from typing import Dict

from .paths import EXPECTED_DATA_PATH
from ..test_support._datetime import fromisoformat_z


class ExpectedData:
    def __init__(self):
        data = json.load(open(EXPECTED_DATA_PATH, "r"))
        self._data = data

    def lookup_item(self, item_id):
        item_data = self.item_data
        item = item_data[item_id]
        return item

    def lookup_document(self, document_id):
        document_data = self.document_data
        doc_dict = document_data[document_id]
        return doc_dict

    def lookup_vault(self, vault_id):
        vault_data = self.vault_data
        vault_dict = vault_data[vault_id]
        return vault_dict

    def lookup_user(self, user_id):
        user_data = self.user_data
        user_dict = user_data[user_id]
        return user_dict

    @property
    def item_data(self) -> Dict[str, Dict]:
        return self._data["items"]

    @property
    def document_data(self) -> Dict[str, Dict]:
        return self._data["documents"]

    @property
    def vault_data(self) -> Dict[str, Dict]:
        return self._data["vaults"]

    @property
    def user_data(self) -> Dict[str, Dict]:
        return self._data["users"]


class ExpectedUser:
    def __init__(self, user_dict: Dict):
        self._data = user_dict

    @property
    def uuid(self) -> str:
        return self._data["uuid"]

    @property
    def created_at(self) -> datetime.datetime:
        created_at = self._data["createdAt"]
        return fromisoformat_z(created_at)

    @property
    def updated_at(self) -> datetime.datetime:
        updated_at = self._data["updatedAt"]
        return fromisoformat_z(updated_at)

    @property
    def last_auth_at(self) -> datetime.datetime:
        updated_at = self._data["lastAuthAt"]
        return fromisoformat_z(updated_at)

    @property
    def email(self) -> str:
        return self._data["email"]

    @property
    def first_name(self) -> str:
        return self._data["firstName"]

    @property
    def last_name(self) -> str:
        return self._data["lastName"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def returncode(self) -> int:
        return self._data["returncode"]


class ExpectedUserData:
    def __init__(self):
        expected_data = ExpectedData()
        user_data: Dict = expected_data.user_data
        self._data: Dict = user_data

    def data_for_user(self, user_identifier: str):
        user_dict = self._data[user_identifier]
        user = ExpectedUser(user_dict)
        return user
