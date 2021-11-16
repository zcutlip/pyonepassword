import json
from typing import Dict
from pytest import fixture
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

    @property
    def item_data(self) -> Dict[str, Dict]:
        return self._data["items"]

    @property
    def document_data(self) -> Dict[str, Dict]:
        return self._data["documents"]

    @property
    def vault_data(self) -> Dict[str, Dict]:
        return self._data["vaults"]


@fixture
def expected_data():
    data = ExpectedData()
    return data
