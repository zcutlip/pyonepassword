from typing import Dict

from pyonepassword.op_items.item_field_base import OPItemField


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
    def item_field(cls, field_dict: Dict, *args):
        item_cls = cls.field_type_lookup(field_dict)

        obj = item_cls(field_dict)
        return obj


def op_register_item_field_type(item_class):
    OPItemFieldFactory.register_op_field_type(item_class)
    return item_class
