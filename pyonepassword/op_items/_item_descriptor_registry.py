from ._item_type_registry import OPItemFactory
from .item_types._item_descriptor_base import OPAbstractItemDescriptor
from .item_types.generic_item import _OPGenericItemDescriptor


class OPItemDescriptorFactory(OPItemFactory):
    _GENERIC_ITEM_CLASS = _OPGenericItemDescriptor
    _TYPE_REGISTRY = {}

    @classmethod
    def item_descriptor(cls, item_json, generic_okay=False) -> OPAbstractItemDescriptor:
        obj = cls.op_item(item_json, generic_okay=generic_okay)
        return obj


def op_register_item_descriptor_type(item_class):
    item_type = item_class.CATEGORY
    OPItemDescriptorFactory.register_op_item_type(item_type, item_class)
    return item_class
