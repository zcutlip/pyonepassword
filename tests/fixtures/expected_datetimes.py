from typing import Dict

from ..test_support._datetime import fromisoformat_z
from .expected_data import ExpectedData


class ExpectedDatetimeData:
    def __init__(self):
        expected_data = ExpectedData()
        datetime_data: Dict = expected_data.datetime_data
        self._data: Dict = datetime_data

    def datetime_for_key(self, datetime_key: str):
        datetime_str = self._data[datetime_key]
        epected_datetime = fromisoformat_z(datetime_str)
        return epected_datetime
