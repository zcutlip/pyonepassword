from typing import Any, Dict, Type

from .item_field_base import OPItemField


class OPItemFieldFactory:
    _TYPE_REGISTRY: Dict[str, Type[OPItemField]] = {}

    @classmethod
    def register_op_field_type(cls, item_class):
        cls._TYPE_REGISTRY[item_class.FIELD_TYPE] = item_class

    @classmethod
    def field_type_lookup(cls, field_dict: Dict[str, Any]):
        item_type = field_dict["type"]
        field_class = OPItemField
        try:
            field_class = cls._TYPE_REGISTRY[item_type]
        except KeyError:
            pass
        return field_class

    @classmethod
    def item_field(cls, field_dict: Dict[str, Any], *args):
        item_cls = cls.field_type_lookup(field_dict)

        obj = item_cls(field_dict)
        return obj


def op_register_item_field_type(item_class):
    OPItemFieldFactory.register_op_field_type(item_class)
    return item_class
