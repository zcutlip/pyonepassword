from __future__ import annotations

from json import JSONDecodeError
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, Union

from ..json import safe_unjson
from ..py_op_exceptions import OPInvalidFieldException
from .item_field_base import OPItemField
from .uuid import OPUniqueIdentifierBase32, is_uuid

if TYPE_CHECKING:
    from .item_section import OPSection  # pragma: no coverage


class OPUnknownFieldTypeException(Exception):
    def __init__(self, msg, item_dict=None):
        super().__init__(msg)
        self.item_dict = item_dict


class OPNewItemField(OPItemField):
    """
    A class for creating new fields for use with new items

    New fields may be created directly, or from existing fields
    """
    FIELD_TYPE: Optional[str] = None
    FIELD_PURPOSE: Optional[str] = None

    def __init__(self, field_label: str, value: Any, field_id=None, section: Optional[OPSection] = None):
        """
        Create a new field object

        NOTE: This class must be subclassed and FIELD_TYPE overridden

        Parameters
        ----------
        field_label: str
            The user-visible name of the field
        field_id: str, optional
            The unique identifier for this field. If none is provided, a random one will be generated
        section: OPSection, optional
            The section this field should be associated with. Not all fields are in sections
        """
        if not self.FIELD_TYPE:  # pragma: no cover
            raise TypeError(
                f"{self.__class__.__name__} must be overridden and FIELD_TYPE set")

        if not field_id:
            unique_id = OPUniqueIdentifierBase32()
            field_id = str(unique_id)
        field_dict = {
            "id": field_id,
            "label": field_label,
            "value": value,
            "type": self.FIELD_TYPE
        }
        if self.FIELD_PURPOSE:
            field_dict["purpose"] = self.FIELD_PURPOSE
        if section:
            field_dict["section"] = dict(section)
        super().__init__(field_dict)
        if section:
            section.register_field(self)

    def update_section(self, section: OPSection):
        """
        Update a field's associated section in the event
        a section's UUID was regenerated
        """
        if self.section_id != section.section_id:
            self["section"] = dict(section)
            section.register_field(self)

    @classmethod
    def from_field(cls, field: OPItemField, section: Optional[OPSection] = None):
        """
        Create a new field from an existing one

        If the existing field's ID is a random ID, a new random ID will be generated

        Parameters
        ----------
        field: OPItemField
            The field object to duplicate
        section: OPSection, optional
            The section this field should be associated with. Not all fields are in sections
        Returns
        -------
        new_field: OPItemField
            The newly created field object
        """
        field_id = field["id"]
        if is_uuid(field_id):
            field_id = str(OPUniqueIdentifierBase32())
        label = field["label"]
        value = field["value"]
        new_field = cls(label, value, field_id=field_id, section=section)
        return new_field


class OPNewItemFieldFactory:
    _TYPE_REGISTRY: Dict[str, Type[OPNewItemField]] = {}

    @classmethod
    def register_op_field_type(cls, item_class):
        cls._TYPE_REGISTRY[item_class.FIELD_TYPE] = item_class

    @classmethod
    def _field_from_dict(cls, field_dict, section):
        item_type = field_dict["type"]

        try:
            item_cls = cls._TYPE_REGISTRY[item_type]
        except KeyError as ke:
            raise OPUnknownFieldTypeException(
                f"Unknown item type {item_type}", item_dict=field_dict) from ke

        return item_cls.from_field(field_dict, section=section)

    @classmethod
    def item_field(cls, item_json_or_dict: Union[str, Dict], section: Optional[OPSection] = None):
        try:
            field_dict = safe_unjson(item_json_or_dict)
        except JSONDecodeError as jdce:
            raise OPInvalidFieldException(
                f"Failed to unserialize field JSON: {jdce}") from jdce
        obj = cls._field_from_dict(field_dict, section)
        return obj


def op_register_new_item_field_type(item_class):
    OPNewItemFieldFactory.register_op_field_type(item_class)
    return item_class
