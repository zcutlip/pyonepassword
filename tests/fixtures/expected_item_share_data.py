from typing import Dict

from .expected_data import ExpectedData


class ExpectedItemShare():

    def __init__(self, item_dict: Dict):
        self._data = item_dict

    @property
    def item_identifier(self) -> str:
        return self._data["item-identifier"]

    @property
    def url(self) -> str:
        return self._data["url"]


class ExpectedItemShareData:
    def __init__(self):
        expected_data = ExpectedData()
        item_share_data: Dict = expected_data.item_share_data
        self._data: Dict = item_share_data

    def data_for_key(self, key: str):
        data_dict = self._data[key]
        data = ExpectedItemShare(data_dict)
        return data
