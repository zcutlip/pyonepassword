import json
import os
import tempfile
from typing import Dict, List

from ._new_field_registry import OPItemFieldFactory
from ._new_fields import OPNewItemField
from .item_section import OPItemField, OPSection, OPSectionCollisionException
from .template_directory import OPTemplateDirectory
from .uuid import OPUniqueIdentifierBase32, is_uuid


class OPNewItemDataCollisionException(Exception):
    pass


class OPNewSection(OPSection):
    def __init__(self, section_label: str, section_id: str = None):
        if not section_id:
            unique_id = OPUniqueIdentifierBase32()
            section_id = str(unique_id)
        section_dict = {
            "id": section_id,
            "label": section_label
        }
        super().__init__(section_dict)

    @classmethod
    def from_section(cls, section: OPSection):
        section_id = section.section_id
        if is_uuid(section_id):
            section_id = str(OPUniqueIdentifierBase32())
        label = section.label
        return cls(label, section_id=section_id)


class OPNewItemMixin:

    def __init__(self, title: str, sections: List[OPSection] = [], fields: List[OPItemField] = [], extra_data={}):
        directory = OPTemplateDirectory()
        template_dict: Dict = directory.template_for_category(self.CATEGORY)
        template_dict["title"] = title
        section_map = {}
        new_sections = []
        new_fields = []

        for section in sections:
            if not isinstance(section, OPNewSection):
                section = OPNewSection.from_section(section)
            if section.section_id in section_map:
                raise OPSectionCollisionException(
                    f"Duplicate section ID when creating new sections: {section.section_id}")
            section_map[section.section_id] = section
            new_sections.append(section)

        for field in fields:
            if not isinstance(field, OPNewItemField):
                section_id = field.section_id
                section = section_map.get(section_id)
                field = OPItemFieldFactory.item_field(field, section)
            new_fields.append(field)
        template_dict["sections"] = new_sections
        template_dict["fields"] = new_fields
        key_collisions = []
        for key in extra_data.keys():
            if key in self:
                key_collisions.append(key)
        if key_collisions:
            raise OPNewItemDataCollisionException(
                f"Extra data key collisions: {key_collisions}")
        if extra_data:
            template_dict.update(extra_data)
        super().__init__(template_dict)
        self._temp_files = []

    def secure_tempfile(self, encoding="utf8") -> str:
        temp = tempfile.NamedTemporaryFile(
            mode="w", delete=False, encoding=encoding)
        self._temp_files.append(temp.name)
        json.dump(self, temp)
        temp.close()
        return temp.name

    def __del__(self):
        while self._temp_files:
            t = self._temp_files.pop()
            try:
                os.unlink(t)
            except FileNotFoundError:
                continue
