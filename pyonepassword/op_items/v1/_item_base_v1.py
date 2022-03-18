import copy
import json
import os
import tempfile
from abc import abstractmethod
from typing import List, Union

from ._item_overview import URLEntry
from .._op_items_base import OPAbstractItem
from ..item_section import OPSectionCollisionException
from ..templates import TemplateDirectory
from ._item_section import OPSectionFieldV1, OPSectionV1


class OPItemTemplateMixin:
    TEMPLATE_ID: str = None
    TEMPLATE_DIRECTORY = TemplateDirectory()

    def __init__(self, *args, **kwargs):
        template_dict = self.TEMPLATE_DIRECTORY.template(self.TEMPLATE_ID)
        template_dict = copy.deepcopy(template_dict)
        item_dict = {
            "details": template_dict
        }
        super().__init__(*args, item_dict, **kwargs)
        self._from_template = True


class OPItemBaseV1(OPAbstractItem):
    TEMPLATE_ID = None
    ITEM_CATEGORY = None

    @abstractmethod
    def __init__(self, item_dict):
        super().__init__(item_dict)
        self._initialize_sections()

    def add_section(self, title: str, fields: List[OPSectionFieldV1] = None, name: str = None):
        if not name:
            name = OPSectionV1.random_section_name()
        for sect in self.sections:
            if sect.name == name:
                raise OPSectionCollisionException(
                    f"Section with the unique name {name} already exists")
        new_sect = OPSectionV1.new_section(name, title, fields)
        sections = self.sections
        sections.append(new_sect)
        self.sections = sections

        return new_sect

    def primary_section_field_value(self, field_label):
        first_sect = self.first_section
        field_value = self._field_value_from_section(first_sect, field_label)
        return field_value

    def set_primary_section_field_value(self, field_label, field_value):
        first_sect = self.first_section
        section_field: OPSectionFieldV1
        section_field = first_sect.fields_by_label(field_label)[0]
        section_field.value = field_value
        self.first_section = first_sect

    @property
    def sections(self) -> List[OPSectionV1]:
        details_dict = self.details
        section_list = details_dict.get("sections", [])

        return section_list

    @sections.setter
    def sections(self, sections: List[OPSectionV1]):
        details_dict = self.details
        details_dict['sections'] = sections

    @property
    def first_section(self) -> OPSectionV1:
        first = None
        if self.sections:
            first = self.sections[0]
            first = OPSectionV1(first)
        return first

    @first_section.setter
    def first_section(self, section: OPSectionV1):
        sections = self.sections
        sections[0] = section
        self.sections = sections

    @property
    def details(self):
        return self._item_dict["details"]

    @property
    def is_from_template(self):
        return self._from_template

    @property
    def category(self):
        if not self.ITEM_CATEGORY:
            raise NotImplementedError(
                f"item category is not set for {self.__class__.__name__}")
        return self.ITEM_CATEGORY

    def sections_by_title(self, title) -> List[OPSectionV1]:
        """
        Returns a list of zero or more sections matching the given title.
        Sections are not required to have unique titles, so there may be more than one match.
        """
        matching_sections = []
        sect: OPSectionV1
        for sect in self.sections:
            if sect.title == title:
                matching_sections.append(sect)

        return matching_sections

    def first_section_by_title(self, title) -> OPSectionV1:
        sections = self.sections_by_title(title)
        section = None
        if sections:
            section = sections[0]
        return section

    def get_details_value(self, field_designation):
        field_value = None
        details_dict = self.details
        field_value = details_dict[field_designation]

        return field_value

    def field_value_by_section_title(self, section_title: str, field_label: str):
        section = self.first_section_by_title(section_title)
        value = self._field_value_from_section(section, field_label)
        return value

    def __del__(self):
        while self._temp_files:
            t = self._temp_files.pop()
            try:
                os.unlink(t)
            except FileNotFoundError:
                continue

    def details_secure_tempfile(self, encoding="utf-8") -> tempfile.NamedTemporaryFile:
        temp = tempfile.NamedTemporaryFile(
            mode="w", delete=False, encoding=encoding)
        self._temp_files.append(temp.name)
        details_json = json.dumps(self.details)
        temp.write(details_json)
        temp.close()
        return temp.name

    @property
    def urls(self):
        return self._overview.url_list()

    def first_url(self) -> Union[URLEntry, None]:
        url = None
        # When creating a new item, we can't specify more than one url
        # so if there's more than one, we have to just grab the first
        urls = self.urls
        if urls:
            url = urls[0]
        return url

    def _field_value_from_section(self, section: OPSectionV1, field_label: str):
        section_field: OPSectionFieldV1 = section.fields_by_label(field_label)[
            0]
        value = section_field.value
        return value

    def _initialize_sections(self):
        section_list = []
        details_dict = self.details
        _sections = details_dict.get("sections")
        if _sections:
            for section_dict in _sections:
                s = OPSectionV1(section_dict)
                section_list.append(s)
        details_dict["sections"] = section_list
