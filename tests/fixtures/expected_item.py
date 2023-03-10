import datetime
from typing import Dict, List

from ..test_support._datetime import fromisoformat_z
from .expected_data import ExpectedData
from .expected_item_fields import ExpectedItemField
from .expected_item_sections import ExpectedItemSection
from .valid_data import ValidData


class ExpectedItemBase:
    def __init__(self, item_dict: Dict):
        self._data = item_dict

    @property
    def unique_id(self) -> str:
        return self._data["id"]

    @property
    def title(self) -> str:
        return self._data["title"]

    @property
    def category(self) -> str:
        return self._data["category"]

    @property
    def created_at(self) -> datetime.datetime:
        created_at = self._data["created_at"]
        return fromisoformat_z(created_at)

    @property
    def updated_at(self) -> datetime.datetime:
        updated_at = self._data["updated_at"]
        return fromisoformat_z(updated_at)

    @property
    def last_edited_by(self) -> str:
        return self._data["last_edited_by"]

    @property
    def vault_id(self) -> str:
        return self._data["vault_id"]

    @property
    def returncode(self) -> int:
        return self._data["returncode"]

    @property
    def archived(self) -> bool:
        return self._data["archived"]

    @property
    def version(self) -> int:
        return self._data["version"]

    @property
    def favorite(self) -> bool:
        return self._data.get("favorite", False)

    def fields_by_label(self, label: str) -> List[ExpectedItemField]:
        """
        Labels aren't guaranteed to so the best we can guarantee is a list,
        even if only one
        """
        fields = []
        field_dicts = self._data["fields"]
        for fd in field_dicts:
            f = ExpectedItemField(fd)
            if f.label == label:
                fields.append(f)
        return fields

    def section_by_id(self, section_id: str) -> ExpectedItemSection:
        section_dict = None
        sections = self._data["sections"]
        for sect in sections:
            if sect["id"] == section_id:
                section_dict = sect
        section = ExpectedItemSection(section_dict)
        return section


class ExpectedItemData(ValidData):
    def __init__(self):
        expected_data = ExpectedData()
        item_data_registry: Dict = expected_data.item_data
        registry = item_data_registry["registry"]
        super().__init__(registry=registry)
        self._data_path = item_data_registry["data_path"]
