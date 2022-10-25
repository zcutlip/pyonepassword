import json
import os
import tempfile
from typing import Dict, List

from ._new_field_registry import OPNewItemFieldFactory
from ._new_fields import OPNewItemField
from .item_field_base import OPItemField
from .item_section import OPSection, OPSectionCollisionException
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

    def __init__(self, title: str, fields: List[OPItemField] = [], sections: List[OPSection] = [], extra_data={}):
        if sections is None:  # pragma: no coverage
            sections = []
        else:
            sections = list(sections)
        if fields is None:  # pragma: no coverage
            fields = []
        else:
            fields = list(fields)
        if extra_data is None:  # pragma: no coverage
            extra_data = {}
        else:
            extra_data = dict(extra_data)

        directory = OPTemplateDirectory()
        template_dict: Dict = directory.template_for_category(self.CATEGORY)
        template_dict["title"] = title
        section_map = {}
        new_sections = []
        new_fields = []
        old_to_new_sections = {}
        for section in sections:
            if not isinstance(section, OPNewSection):
                old_id = section.section_id
                section = OPNewSection.from_section(section)
                # create a mapping of old-to-new sections to keep
                # up with the sections whose UUIDs get regenerated
                old_to_new_sections[old_id] = section
            if section.section_id in section_map:
                raise OPSectionCollisionException(
                    f"Duplicate section ID when creating new sections: {section.section_id}")
            section_map[section.section_id] = section
            new_sections.append(section)

        for field in fields:
            section_id = field.section_id
            if not isinstance(field, OPNewItemField):
                section = old_to_new_sections.get(section_id)
                field = OPNewItemFieldFactory.item_field(field, section)
            else:
                section = old_to_new_sections.get(section_id)
                if section:
                    # If a section's UUID may have been regenerated, we need to re-link it to the field
                    field.update_section(section)
            new_fields.append(field)
        template_dict["sections"] = new_sections
        template_dict["fields"] = new_fields
        key_collisions = []
        for key in extra_data.keys():
            if key in self:
                key_collisions.append(key)  # pragma: no coverage
        if key_collisions:
            raise OPNewItemDataCollisionException(  # pragma: no coverage
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

        # if we blow up during object initialization
        # _temp_files may not exist, so check first
        if hasattr(self, "_temp_files"):
            while self._temp_files:
                t = self._temp_files.pop()
                try:
                    os.unlink(t)
                except FileNotFoundError:
                    continue
