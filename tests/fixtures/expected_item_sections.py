from typing import Dict

from .expected_data import ExpectedData


class ExpectedItemSection:

    def __init__(self, item_section: Dict) -> None:
        self._data = item_section

    @property
    def section_id(self) -> str:
        return self._data["id"]

    @property
    def label(self) -> str:
        return self._data["label"]


class ExpectedItemSectionData:

    def __init__(self) -> None:
        expected_data = ExpectedData()
        section_data: Dict = expected_data.item_sections
        self._data: Dict = section_data

    def data_for_key(self, key):
        data = self._data[key]
        data = ExpectedItemSection(data)
        return data
