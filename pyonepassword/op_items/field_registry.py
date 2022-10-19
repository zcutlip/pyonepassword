from json.decoder import JSONDecodeError
from typing import Dict, Union

from pyonepassword.op_items.item_field_base import OPItemField

from ..json import safe_unjson
from ..py_op_exceptions import OPInvalidFieldException


class OPItemFieldFactory:
    _TYPE_REGISTRY = {}

    @classmethod
    def register_op_field_type(cls, item_class):
        cls._TYPE_REGISTRY[item_class.FIELD_TYPE] = item_class

    @classmethod
    def field_type_lookup(cls, field_dict):
        item_type = field_dict["type"]
        field_class = None
        try:
            field_class = cls._TYPE_REGISTRY[item_type]
        except KeyError:
            field_class = OPItemField
        return field_class

    @classmethod
    def _field_from_dict(cls, field_dict):
        item_cls = cls.field_type_lookup(field_dict)

        return item_cls(field_dict)

    @classmethod
    def item_field(cls, item_json_or_dict: Union[str, Dict], *args):
        try:
            field_dict = safe_unjson(item_json_or_dict)
        except JSONDecodeError as jdce:
            raise OPInvalidFieldException(
                f"Failed to unserialize field JSON: {jdce}") from jdce
        obj = cls._field_from_dict(field_dict, *args)
        return obj


def op_register_item_field_type(item_class):
    OPItemFieldFactory.register_op_field_type(item_class)
    return item_class
