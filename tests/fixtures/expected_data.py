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

    @property
    def item_data(self) -> Dict[str, Dict]:
        return self._data["items"]


@fixture
def expected_data():
    data = ExpectedData()
    return data
