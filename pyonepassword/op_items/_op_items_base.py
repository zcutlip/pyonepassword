from abc import ABC, abstractmethod
from typing import List
from .item_section import OPSection, OPSectionField


class OPAbstractItem(ABC):
    TEMPLATE_ID = None

    @abstractmethod
    def __init__(self, item_dict):
        self._item_dict = item_dict

    def primary_section_field_value(self, field_label):
        first_sect = self.first_section
        field_value = self._field_value_from_section(first_sect, field_label)
        return field_value

    @property
    def uuid(self) -> str:
        return self._item_dict["uuid"]

    @property
    def title(self) -> str:
        overview = self._item_dict["overview"]
        title = overview["title"]
        return title

    @property
    def sections(self) -> List[OPSection]:
        section_list = []
        _sections = self._item_dict['details'].get("sections")
        if _sections:
            for section_dict in _sections:
                s = OPSection(section_dict)
                section_list.append(s)
        return section_list

    @property
    def first_section(self) -> OPSection:
        first = None
        if self.sections:
            first = self.sections[0]
            first = OPSection(first)
        return first

    def sections_by_title(self, title) -> List[OPSection]:
        """
        Returns a list of zero or more sections matching the given title.
        Sections are not required to have unique titles, so there may be more than one match.
        """
        matching_sections = []
        sect: OPSection
        for sect in self.sections:
            if sect.title == title:
                matching_sections.append(sect)

        return matching_sections

    def first_section_by_title(self, title) -> OPSection:
        # TODO: handle case of no matching section titles
        sections = self.sections_by_title(title)
        section = sections[0]
        return section

    def get_item_field_value(self, field_designation):
        field_value = None
        details = self._item_dict["details"]
        field_value = details[field_designation]

        return field_value

    def field_value_by_section_title(self, section_title: str, field_label: str):
        section = self.first_section_by_title(section_title)
        value = self._field_value_from_section(section, field_label)
        return value

    def _field_value_from_section(self, section: OPSection, field_label: str):
        section_field: OPSectionField = section.fields_by_label(field_label)[0]
        value = section_field.value
        return value
