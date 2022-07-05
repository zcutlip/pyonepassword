from typing import Dict, Union

from .expected_data import ExpectedData


class ExpectedItemField:

    def __init__(self, item_field: Dict):
        self._data = item_field

    @property
    def field_id(self) -> str:
        return self._data["id"]

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def purpose(self) -> str:
        return self._data["purpose"]

    @property
    def label(self) -> str:
        return self._data["label"]

    @property
    def value(self) -> Union[str, Dict]:
        return self._data["value"]

    @property
    def reference(self) -> str:
        return self._data["reference"]

    @property
    def entropy(self) -> float:
        return self._data["entropy"]


class ExpectedItemFieldData:

    def __init__(self) -> None:
        expected_data = ExpectedData()
        field_data: Dict = expected_data.item_fields
        self._data: Dict = field_data

    def data_for_key(self, key):
        data = self._data[key]
        data = ExpectedItemField(data)
        return data
