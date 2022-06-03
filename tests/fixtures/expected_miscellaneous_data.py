from typing import Dict

from .expected_data import ExpectedData


class ExpectedMiscData:
    def __init__(self):
        expected_data = ExpectedData()
        datetime_data: Dict = expected_data.misc_data
        self._data: Dict = datetime_data

    def data_for_key(self, key: str):
        data = self._data[key]
        return data
