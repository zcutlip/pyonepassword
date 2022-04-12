from ._op_item_type_registry import OPItemFactory


class OPItemDescriptorFactory(OPItemFactory):
    _TYPE_REGISTRY = {}

    @classmethod
    def item_descriptor(cls, item_json):
        obj = cls.op_item(item_json)
        return obj


def op_register_item_descriptor_type(item_class):
    item_type = item_class.TEMPLATE_ID
    OPItemDescriptorFactory.register_op_item_type(item_type, item_class)
    return item_class
