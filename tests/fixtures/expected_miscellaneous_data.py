from typing import Dict

from .expected_data import ExpectedData


class ExpectedMiscData:
    def __init__(self):
        expected_data = ExpectedData()
        misc_data: Dict = expected_data.misc_data
        self._data: Dict = misc_data

    def data_for_key(self, key: str):
        data = self._data[key]
        return data
