from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type


@op_register_item_descriptor_type
class OPIdentityItemDescriptor(OPAbstractItemDescriptor):
    CATEGORY = "IDENTITY"

    def __init__(self, item_dict):
        super().__init__(item_dict)
