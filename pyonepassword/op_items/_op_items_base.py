import copy
import os

from abc import abstractmethod, abstractproperty
from typing import List, Union

from .._datetime import fromisoformat_z
from ._item_descriptor_base import OPAbstractItemDescriptor
from .item_section import OPSection, OPSectionField


class URLEntry(dict):
    def __init__(self, url_dict):
        ud = copy.deepcopy(url_dict)
        super().__init__(ud)

    @abstractproperty
    def label(self):
        pass

    @abstractproperty
    def url(self):
        pass


class OPAbstractItem(OPAbstractItemDescriptor):
    TEMPLATE_ID = None
    ITEM_CATEGORY = None

    @abstractmethod
    def __init__(self, item_dict):
        super().__init__(item_dict)
        self._temp_files = []

    @abstractmethod
    def add_section(self, title: str, fields: List[OPSectionField] = None, name: str = None):
        pass

    @abstractmethod
    def primary_section_field_value(self, field_label):
        pass

    def set_primary_section_field_value(self, field_label, field_value):
        first_sect = self.first_section
        section_field: OPSectionField
        section_field = first_sect.fields_by_label(field_label)[0]
        section_field.value = field_value
        self.first_section = first_sect

    @abstractproperty
    def sections(self) -> List[OPSection]:
        pass

    @sections.setter
    def sections(self, sections: List[OPSection]):
        details_dict = self.details
        details_dict['sections'] = sections

    @abstractproperty
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
        if not self.ITEM_CATEGORY:
            raise NotImplementedError(
                f"item category is not set for {self.__class__.__name__}")
        return self.ITEM_CATEGORY

    @abstractmethod
    def sections_by_title(self, title) -> List[OPSection]:
        """
        Returns a list of zero or more sections matching the given title.
        Sections are not required to have unique titles, so there may be more than one match.
        """
        pass

    @abstractmethod
    def first_section_by_title(self, title) -> OPSection:
        pass

    @abstractmethod
    def field_value_by_section_title(self, section_title: str, field_label: str):
        pass

    def __del__(self):
        while self._temp_files:
            t = self._temp_files.pop()
            try:
                os.unlink(t)
            except FileNotFoundError:
                continue

    @abstractproperty
    def urls(self):
        pass

    @abstractmethod
    def first_url(self) -> Union[URLEntry, None]:
        pass


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
