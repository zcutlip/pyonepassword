import copy
import json
import os
import tempfile

from abc import abstractmethod
from typing import List, Union

from .._datetime import fromisoformat_z
from ._item_overview import OPItemOverview, URLEntry
from ._item_descriptor_base import OPAbstractItemDescriptor
from .item_section import OPSection, OPSectionField, OPSectionCollisionException
from .templates import TemplateDirectory


class OPFieldNotFoundException(Exception):
    pass


class OPMutableItemOverview(OPItemOverview):

    def set_url(self, url, label=""):
        url_dict = {
            "l": label,
            "u": url
        }
        # TODO: is it an error if we alread have one or more URLs?
        new_url = URLEntry(url_dict)
        self["URLs"] = [new_url]


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


class OPAbstractItem(OPAbstractItemDescriptor):
    CATEGORY = None

    @abstractmethod
    def __init__(self, item_dict_or_json):
        super().__init__(item_dict_or_json)
        self._temp_files = []
        self._initialize_sections()
        self._field_map = self._initialize_fields()

    def add_section(self, title: str, fields: List[OPSectionField] = None, name: str = None):
        if not name:
            name = OPSection.random_section_name()
        for sect in self.sections:
            if sect.name == name:
                raise OPSectionCollisionException(
                    f"Section with the unique name {name} already exists")
        new_sect = OPSection.new_section(name, title, fields)
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
        section_field: OPSectionField
        section_field = first_sect.fields_by_label(field_label)[0]
        section_field.value = field_value
        self.first_section = first_sect

    @property
    def sections(self) -> List[OPSection]:
        section_list = self.get("sections", [])
        return section_list

    @sections.setter
    def sections(self, sections: List[OPSection]):
        details_dict = self.details
        details_dict['sections'] = sections

    @property
    def first_section(self) -> OPSection:
        first = None
        if self.sections:
            first = self.sections[0]
            first = OPSection(first)
        return first

    @first_section.setter
    def first_section(self, section: OPSection):
        sections = self.sections
        sections[0] = section
        self.sections = sections

    @property
    def is_from_template(self):
        return self._from_template

    @property
    def category(self):
        if not self.CATEGORY:
            raise NotImplementedError(
                f"item category is not set for {self.__class__.__name__}")
        return self.CATEGORY.lower()

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
        sections = self.sections_by_title(title)
        section = None
        if sections:
            section = sections[0]
        return section

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

    def field_by_id(self, field_id) -> OPSectionField:
        try:
            field = self._field_map[field_id]
        except KeyError:
            raise OPFieldNotFoundException(
                f"Field not found with ID: {field_id}")
        return field

    def field_value_by_id(self, field_id):
        field = self.field_by_id(field_id)
        value = field.value
        return value

    def _field_value_from_section(self, section: OPSection, field_label: str):
        section_field: OPSectionField = section.fields_by_label(field_label)[0]
        value = section_field.value
        return value

    def _initialize_sections(self):
        section_list = []
        _sections = self.get("sections")
        if _sections:
            for section_dict in _sections:
                s = OPSection(section_dict)
                section_list.append(s)
        self["sections"] = section_list

    def _initialize_fields(self):
        field_list = []
        field_map = {}
        _fields = self.get("fields", [])
        for field_dict in _fields:
            field = OPSectionField(field_dict, deep_copy=False)
            field_list.append(field)
            field_map[field.field_id] = field
        self["fields"] = field_list
        return field_map


class OPItemCreateResult(dict):

    def __init__(self, result_dict):
        super().__init__(result_dict)

    @property
    def uuid(self):
        return self["uuid"]

    @property
    def vault_uuid(self):
        return self["vaultUuid"]

    @property
    def created_at(self):
        created = self["createdAt"]
        created = fromisoformat_z(created)
        return created

    @property
    def updated_at(self):
        updated = self["updatedAt"]
        updated = fromisoformat_z(updated)
        return updated
