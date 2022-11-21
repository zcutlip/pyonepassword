from abc import abstractmethod
from typing import List, Optional

from ._item_descriptor_base import OPAbstractItemDescriptor
from .field_registry import OPItemFieldFactory
from .item_field_base import OPItemField
from .item_section import (
    OPItemFieldCollisionException,
    OPSection,
    OPSectionCollisionException
)


class OPSectionNotFoundException(Exception):
    pass


class OPFieldNotFoundException(Exception):
    pass


class OPAbstractItem(OPAbstractItemDescriptor):
    CATEGORY: Optional[str] = None

    @abstractmethod
    def __init__(self, item_dict_or_json):
        super().__init__(item_dict_or_json)
        self._section_map = self._initialize_sections()
        self._field_map = self._initialize_fields()

    @property
    def sections(self) -> List[OPSection]:
        section_list = self.get("sections", [])
        return section_list

    def sections_by_label(self, label, case_sensitive=True) -> List[OPSection]:
        """
        Returns a list of zero or more sections matching the given title.
        Sections are not required to have unique titles, so there may be more than one match.
        """
        matching_sections = []
        sect: OPSection
        for sect in self.sections:
            s_label = sect.label
            if not case_sensitive:
                s_label = s_label.lower()
                label = label.lower()
            if s_label == label:
                matching_sections.append(sect)

        return matching_sections

    def section_by_id(self, section_id) -> OPSection:
        try:
            section: OPSection = self._section_map[section_id]
        except KeyError:
            raise OPSectionNotFoundException(
                f"Section not found with Section ID: {section_id}")

        return section

    def first_section_by_label(self, label, case_sensitive=True) -> Optional[OPSection]:
        sections = self.sections_by_label(label, case_sensitive=case_sensitive)
        section = None
        if sections:
            section = sections[0]
        return section

    def field_value_by_section_title(self, section_title: str, field_label: str):
        section = self.first_section_by_label(section_title)
        value = None
        if section is not None:
            value = self._field_value_from_section(section, field_label)
        return value

    def field_by_id(self, field_id) -> OPItemField:
        try:
            field = self._field_map[field_id]
        except KeyError:
            raise OPFieldNotFoundException(
                f"Field not found with ID: {field_id}")
        return field

    def fields_by_label(self, field_label: str, case_sensitive=True) -> List[OPItemField]:
        fields = []
        f: OPItemField
        for _, f in self._field_map.items():
            f_label = f.label
            if not case_sensitive:
                f_label = f_label.lower()
                field_label = field_label.lower()

            if f_label == field_label:
                fields.append(f)
        return fields

    def first_field_by_label(self, field_label: str, case_sensitive=True) -> OPItemField:
        fields = self.fields_by_label(
            field_label, case_sensitive=case_sensitive)
        f = fields[0]
        return f

    def field_value_by_id(self, field_id):
        field = self.field_by_id(field_id)
        value = field.value
        return value

    def field_reference_by_id(self, field_id) -> Optional[str]:
        field = self.field_by_id(field_id)
        ref = field.reference
        return ref

    def _field_value_from_section(self, section: OPSection, field_label: str):
        section_field: OPItemField = section.fields_by_label(field_label)[0]
        value = section_field.value
        return value

    def _initialize_sections(self):
        section_list = []
        section_map = {}
        _sections = self.get("sections")
        if _sections:
            for section_dict in _sections:
                s = OPSection(section_dict)
                section_id = s.section_id
                if section_id in section_map:
                    raise OPSectionCollisionException(
                        f"Section {section_id} already registered")
                section_map[section_id] = s
                section_list.append(s)
        self["sections"] = section_list
        return section_map

    def _initialize_fields(self):
        field_list = []
        field_map = {}
        _fields = self.get("fields", [])
        for field_dict in _fields:
            field = OPItemFieldFactory.item_field(field_dict)
            field_id = field.field_id
            if field_id in field_map:
                raise OPItemFieldCollisionException(
                    f"Field {field_id} already registered")
            section_dict = field.get("section")
            if section_dict:
                section_id = section_dict["id"]
                section = self.section_by_id(section_id)
                section.register_field(field_dict)
            field_list.append(field)
            field_map[field.field_id] = field
        self["fields"] = field_list
        return field_map
