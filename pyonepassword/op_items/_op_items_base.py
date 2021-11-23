import copy
import json
import os
import tempfile

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Union
from .item_section import OPSection, OPSectionField, OPSectionCollisionException
from .templates import TemplateDirectory


class OPItemOverview(dict):
    class URLEntry(dict):
        def __init__(self, url_dict):
            ud = copy.deepcopy(url_dict)
            super().__init__(ud)

        @property
        def label(self):
            return self["l"]

        @property
        def url(self):
            return self["u"]

    def __init__(self, overview_dict):
        od = copy.deepcopy(overview_dict)
        super().__init__(od)
        _urls = self._process_urls()
        if _urls is not None:
            self["URLs"] = _urls

    def _process_urls(self):
        # Some item types, namely Login and Password can
        # have a URLs dict in their overview
        # other item types do not. We want to make accessing those
        # transparent, making them available if they exist, but not
        # failing if they don't
        url_items = None
        url_dicts = self.get("URLs", [])
        if url_dicts:
            url_items = []
            for d in url_dicts:
                url = self.URLEntry(d)
                url_items.append(url)
        return url_items

    def url_list(self):
        return self.get("URLs", None)

    def set_url(self, url, label=""):
        url_dict = {
            "l": label,
            "u": url
        }
        # TODO: is it an error if we alread have one or more URLs?
        new_url = self.URLEntry(url_dict)
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


class OPAbstractItem(ABC):
    TEMPLATE_ID = None
    ITEM_CATEGORY = None

    @abstractmethod
    def __init__(self, item_dict):
        self._from_template = False
        self._item_dict = item_dict
        # not every item has an overview
        # in particular, items created from a template do not
        overview = self._item_dict.get("overview", {})
        self._overview = OPItemOverview(overview)
        self._temp_files = []

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
            raise NotImplementedError(
                f"item category is not set for {self._class__.__name__}")
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

    def first_url(self) -> Union[OPItemOverview.URLEntry, None]:
        url = None
        # When creating a new item, we can't specify more than one url
        # so if there's more than one, we have to just grab the first
        urls = self.urls
        if urls:
            url = urls[0]
        return url

    def _field_value_from_section(self, section: OPSection, field_label: str):
        section_field: OPSectionField = section.fields_by_label(field_label)[0]
        value = section_field.value
        return value


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
        created = datetime.fromisoformat(created)
        return created

    @property
    def updatedAt(self):
        updated = self["updatedAt"]
        updated = datetime.fromisoformat(updated)
        return updated
