import json

from typing import Dict

from .paths import EXPECTED_DATA_PATH


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
