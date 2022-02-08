from ._op_item_type_registry import OPItemFactory


class OPItemDescriptorFactory(OPItemFactory):
    _TYPE_REGISTRY = {}
    pass

    @classmethod
    def item_descriptor_from_dict(cls, item_dict):
        obj = cls.op_item_from_item_dict(item_dict)
        return obj

    @classmethod
    def item_descriptor_from_json(cls, item_json):
        obj = cls.op_item_from_json(item_json)
        return obj


def op_register_item_descriptor_type(item_class):
    item_type = item_class.TEMPLATE_ID
    OPItemDescriptorFactory.register_op_item_type(item_type, item_class)
    return item_class
