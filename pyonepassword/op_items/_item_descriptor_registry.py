from ._item_descriptor_base import OPAbstractItemDescriptor
from ._op_item_type_registry import OPItemFactory
from .generic_item import _OPGenericItemDescriptor


class OPItemDescriptorFactory(OPItemFactory):
    _GENERIC_ITEM_CLASS = _OPGenericItemDescriptor
    _TYPE_REGISTRY = {}

    @classmethod
    def item_descriptor(cls, item_json, generic_item=False) -> OPAbstractItemDescriptor:
        obj = cls.op_item(item_json, generic_item=generic_item)
        return obj


def op_register_item_descriptor_type(item_class):
    item_type = item_class.CATEGORY
    OPItemDescriptorFactory.register_op_item_type(item_type, item_class)
    return item_class
