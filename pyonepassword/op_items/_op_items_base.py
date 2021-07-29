import base64
import copy
import json

from abc import ABC, abstractmethod
from typing import Dict, List
from .item_section import OPSection, OPSectionField, OPSectionCollisionException
from .templates import TemplateDirectory

def item_template(cls):
    orig_init = cls.__init__
    t = TemplateDirectory()
    template_dict = t.template(cls.TEMPLATE_ID)

    def __init__(self, *args, **kwargs):
        item_dict = {
            "details": template_dict
        }
        orig_init(self, *args, item_dict, **kwargs)
        self._from_template = True
    cls.__init__ = __init__
    return cls


class OPAbstractItem(ABC):
    TEMPLATE_ID = None
    ITEM_CATEGORY = None

    @abstractmethod
    def __init__(self, item_dict):
        self._from_template = False
        self._item_dict = item_dict

    def add_section(self, title: str, fields: List[OPSectionField] = None, name: str = None):
        if not name:
            name = OPSection.random_section_name()
        for sect in self.sections:
            if sect.name == name:
                raise OPSectionCollisionException(f"Section with the unique name {name} already exists")
        new_sect = OPSection.new_section(name, title, fields)
        sections = self.sections
        sections.append(new_sect)
        self.sections = sections

        return new_sect

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

    @sections.setter
    def sections(self, sections: List[OPSection]):
        self._item_dict['details']['sections'] = sections

    @property
    def first_section(self) -> OPSection:
        first = None
        if self.sections:
            first = self.sections[0]
            first = OPSection(first)
        return first

    @property
    def details(self):
        return self._item_dict["details"]

    @property
    def is_from_template(self):
        return self._from_template

    @property
    def category(self):
        if not self.ITEM_CATEGORY:
            raise NotImplementedError(f"item category is not set for {self._class__.__name__}")
        return self.ITEM_CATEGORY

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

    def b64_encoded_details(self, encoding: str):
        details_json = json.dumps(self.details)
        details_bytes = details_json.encode(encoding)
        b64_details = base64.urlsafe_b64encode(details_bytes)
        b64_details = b64_details.decode(encoding)
        b64_details = b64_details.rstrip('=')
        return b64_details

    def _field_value_from_section(self, section: OPSection, field_label: str):
        section_field: OPSectionField = section.fields_by_label(field_label)[0]
        value = section_field.value
        return value

class OPItemOverview(dict):

    def __init__(self, overview_dict: Dict):
        od = copy.deepcopy(overview_dict)
        super().__init__(od)
