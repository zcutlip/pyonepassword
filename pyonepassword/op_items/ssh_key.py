from typing import Optional

from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem


@op_register_item_descriptor_type
class OPSSHKeyItemDescriptor(OPAbstractItemDescriptor):
    CATEGORY = "SSH_KEY"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def fingerprint(self) -> str:
        return self["additional_information"]


@op_register_item_type
class OPSSHKeyItem(OPAbstractItem):
    CATEGORY = "SSH_KEY"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def public_key(self) -> str:
        password = self.field_value_by_id("public_key")
        return password

    @property
    def public_key_reference(self) -> Optional[str]:
        password = self.field_reference_by_id("public_key")
        return password

    @property
    def fingerprint(self) -> str:
        return self.field_value_by_id("fingerprint")

    @property
    def fingerprint_reference(self) -> Optional[str]:
        return self.field_reference_by_id("fingerprint")

    @property
    def private_key(self) -> str:
        return self.field_value_by_id("private_key")

    @property
    def private_key_reference(self) -> Optional[str]:
        return self.field_reference_by_id("private_key")

    @property
    def key_type(self) -> str:
        return self.field_value_by_id("key_type")

    @property
    def key_type_reference(self) -> Optional[str]:
        return self.field_reference_by_id("key_type")
