from ._item_descriptor_base import OPAbstractItemDescriptor
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem
from ._item_descriptor_registry import op_register_item_descriptor_type


@op_register_item_descriptor_type
class OPLoginDescriptorItem(OPAbstractItemDescriptor):
    CATEGORY = "LOGIN"

    def __init__(self, item_dict):
        super().__init__(item_dict)


@op_register_item_type
class OPLoginItem(OPAbstractItem):
    CATEGORY = "LOGIN"

    @property
    def username(self):
        username = self.field_value_by_id("username")
        return username

    @property
    def password(self):
        password = self.field_value_by_id("password")
        return password
