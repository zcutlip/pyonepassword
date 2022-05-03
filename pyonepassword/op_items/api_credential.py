from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem


@op_register_item_descriptor_type
class OPAPICredentialItemDescriptor(OPAbstractItemDescriptor):
    CATEGORY = "API_CREDENTIAL"

    def __init__(self, item_dict):
        super().__init__(item_dict)


@op_register_item_type
class OPAPICredentialItem(OPAbstractItem):
    CATEGORY = "API_CREDENTIAL"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def username(self):
        username = self.field_value_by_id("username")
        return username

    @property
    def credential(self) -> str:
        cred = self.field_value_by_id("credential")
        return cred
