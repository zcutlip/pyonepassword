from typing import Dict, List, Optional, Union

from ..._abc_meta import enforcedmethod
from ..._py_op_deprecation import deprecated
from ...py_op_exceptions import OPInvalidItemException
from ..field_registry import OPItemFieldFactory
from ..fields_sections.item_field_base import OPItemField
from ..fields_sections.item_section import (
    OPFieldNotFoundException,
    OPItemFieldCollisionException,
    OPSection,
    OPSectionCollisionException
)
from ..item_validation_policy import get_relaxed_validation
from ._item_descriptor_base import OPAbstractItemDescriptor


class OPSectionNotFoundException(Exception):
    pass


class OPAbstractItem(OPAbstractItemDescriptor):
    CATEGORY: Optional[str] = None
    FROM_TEMPLATE = False
    # relaxed validation is disabled by default
    # may be overridden in a "relaxed" sublcass
    # E.g. OPLoginItemRelaxedValidation
    _relaxed_validation: bool = False

    @enforcedmethod
    def __init__(self, item_dict_or_json: Union[Dict, str]):
        super().__init__(item_dict_or_json)
        self._section_map = self._initialize_sections()
        self._field_map = self._initialize_fields()

    @property
    def sections(self) -> List[OPSection]:
        section_list = self.get("sections", [])
        return section_list

    def relaxed_validation(self) -> bool:
        """
        Get relaxed validation policy

        May be determined by any of the following:
        - This class has relaxed validation enabled (e.g., OPLoginItemRelaxedValidation)
        - Relaxed validation is globally set for this class via OPItemValidationPolicy
        - Relaxed validation is globally set for all op item classes

        Returns
        -------
        bool
            Whether relaxed validation policy is enabled
        """
        relaxed = False
        if not self.FROM_TEMPLATE:
            relaxed = self._relaxed_validation
            if not relaxed:
                relaxed = get_relaxed_validation(item_class=self.__class__)
        return relaxed

    def sections_by_label(self, section_label: str, case_sensitive: bool = True) -> List[OPSection]:
        """
        Returns a list of one or more sections matching the given label.

        Note: Sections are not required to have unique labels, so there may be more than one match.

        Parameters
        ----------
        section_label : str
            The user-visible label string to search for
        case_sensitive : bool, optional
            Match section labels case-sensitively, by default True

        Returns
        -------
        List[OPSection]
            The list of matching sections

        Raises
        ------
        OPSectionNotFoundException
            If no sections are found matching the given label
        """
        matching_sections = []
        sect: OPSection
        for sect in self.sections:
            s_label = sect.label
            if not case_sensitive:
                s_label = s_label.lower()
                section_label = section_label.lower()
            if s_label == section_label:
                matching_sections.append(sect)

        if not matching_sections:
            raise OPSectionNotFoundException(
                f"No sections found with label '{section_label}'")
        return matching_sections

    def section_by_id(self, section_id) -> OPSection:
        try:
            section: OPSection = self._section_map[section_id]
        except KeyError:
            raise OPSectionNotFoundException(
                f"Section not found with Section ID: {section_id}")

        return section

    def first_section_by_label(self, section_label, case_sensitive=True) -> Optional[OPSection]:
        """
        Convenience function to return the first matching section

        Note: Sections are not required to have unique labels, so there may be more than one match.

        Parameters
        ----------
        label : str
            The user-visible label string to search for
        case_sensitive : bool, optional
            Match section labels case-insensitively, by default True

        Returns
        -------
        OPSection
            The matching section
        Raises
        ------
        OPSectionNotFoundException
            If no matching sections are found
        """
        sections = self.sections_by_label(
            section_label, case_sensitive=case_sensitive)
        section = None
        if sections:
            section = sections[0]
        return section

    def field_value_by_section_label(self, section_label: str, field_label: str):
        section = self.first_section_by_label(section_label)
        value = None
        if section is not None:
            value = self._field_value_from_section(section, field_label)
        return value

    @deprecated("use item.field_value_by_section_label")
    def field_value_by_section_title(self, section_title: str, field_label: str):
        return self.field_value_by_section_label(section_title, field_label)  # pragma: no coverage

    def field_by_id(self, field_id) -> OPItemField:
        try:
            field = self._field_map[field_id]
        except KeyError:
            raise OPFieldNotFoundException(
                f"Field not found with ID: {field_id}")
        return field

    def fields_by_label(self, field_label: str, case_sensitive=True) -> List[OPItemField]:
        """
        Returns a list of one or more fields matching the given label

        Note: Field labels are not guaranteed to be unique, so more than one field may be returned
        Parameters
        ----------
        label : str
            The user-visible label string to search for
        case_sensitive : bool, optional
            Match field labels case-sensitively, by default True

        Returns
        -------
        List[OPItemField]
            The list of matching fields

        Raises
        ------
        OPFieldNotFoundException
            If no matching fields are found
        """
        fields = []
        f: OPItemField
        for _, f in self._field_map.items():
            f_label = f.label
            if not case_sensitive:
                f_label = f_label.lower()
                field_label = field_label.lower()

            if f_label == field_label:
                fields.append(f)
        if not fields:
            raise OPFieldNotFoundException(
                f"No fields found by label '{field_label}'")
        return fields

    def first_field_by_label(self, field_label: str, case_sensitive=True) -> OPItemField:
        """
        Convenience function to return the first matching field

        Note: field labels are not guaranteed to be unique, or in a particular order, so there may
        be more than one match, in which case the first is returned

        Parameters
        ----------
        label : str
            The user-visible label string to search for
        case_sensitive : bool, optional
            Match field labels case-insensitively, by default True

        Returns
        -------
        OPItemField
            The matching field
        Raises
        ------
        OPFieldNotFoundException
            If no matching fields are found
        """
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
                try:
                    section_id = s.section_id
                except KeyError as e:
                    # in rare instances sections may lack an "id" altogether
                    # Let's treat that as having an empty string instead, since we have
                    # logic to deal with that below, and sometimes that occurs as well
                    if self.relaxed_validation():
                        section_id = ""
                    else:
                        raise OPInvalidItemException(
                            f"section has no ID {s}") from e

                if section_id in section_map:
                    # NOTE: in rare cases 'op' will return items
                    # that have multiple duplicated sections, including section ID
                    # resulting in section ID collisions. In these cases
                    # relaxed validation is required to parse the dictionary
                    # and return a usable object
                    # see:
                    # tests/test_non_conformant_data/test_duplicate_sections.py
                    # if relaxed validation is not enabled
                    # raise an exception
                    if not self.relaxed_validation():
                        raise OPSectionCollisionException(
                            f"Section {section_id} already registered")
                    else:
                        # for code coverage visibility
                        pass
                section_map[section_id] = s
                section_list.append(s)
        self["sections"] = section_list
        return section_map

    def _initialize_fields(self):
        relaxed_validation = self.relaxed_validation()
        field_list = []
        field_map = {}
        _fields = self.get("fields", [])
        for field_dict in _fields:
            field = OPItemFieldFactory.item_field(field_dict)
            try:
                field_id = field.field_id
            except KeyError as e:
                # Based on evidence of sections occasionally lacking "id" elements,
                # in theory there may be instances where fields also lack an "id"
                # Let's treat that as having an empty string instead, since we have
                # logic to deal with that below, and sometimes that occurs as well
                if self.relaxed_validation():
                    field_id = ""
                else:
                    raise OPInvalidItemException(
                        f"Field has no ID: {field.label}") from e
            if field_id in field_map:
                # NOTE: in many cases 'op' will return items
                # that have multiple fields with empty-string IDs
                # resulting in field ID collisions. In these cases
                # relaxed validation is required to parse the dictionary
                # and return a usable object

                # if relaxed validation is not enabled
                # raise an exception
                if not relaxed_validation:
                    raise OPItemFieldCollisionException(
                        f"Field {field_id} already registered")
                else:
                    # for code coverage visibility
                    pass
            section_dict = field.get("section")
            if section_dict:
                section_id = section_dict["id"]
                section = self.section_by_id(section_id)
                section.register_field(
                    field_dict, relaxed_validation=relaxed_validation)
            field_list.append(field)
            field_map[field_id] = field
        self["fields"] = field_list
        return field_map
