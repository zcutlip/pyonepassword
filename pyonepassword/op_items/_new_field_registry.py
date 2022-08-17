from json.decoder import JSONDecodeError
from typing import Dict, Union

from ..json import safe_unjson
from ..py_op_exceptions import OPInvalidFieldException
from .item_section import OPSection


class OPUnknownFieldTypeException(Exception):
    def __init__(self, msg, item_dict=None):
        super().__init__(msg)
        self.item_dict = item_dict


class OPItemFieldFactory:
    _TYPE_REGISTRY = {}

    @classmethod
    def register_op_field_type(cls, item_type, item_class):
        cls._TYPE_REGISTRY[item_type] = item_class

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
    def item_field(cls, item_json_or_dict: Union[str, Dict], section: OPSection = None):
        try:
            field_dict = safe_unjson(item_json_or_dict)
        except JSONDecodeError as jdce:
            raise OPInvalidFieldException(
                f"Failed to unserialize field JSON: {jdce}") from jdce
        obj = cls._field_from_dict(field_dict)
        return obj


def op_register_item_field_type(item_class):
    item_type = item_class.FIELD_TYPE
    OPItemFieldFactory.register_op_field_type(item_type, item_class)
    return item_class
