from typing import Union

from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem, OPFieldNotFoundException

@op_register_item_descriptor_type
class OPDatabaseItemDescriptor(OPAbstractItemDescriptor):
    CATEGORY = "DATABASE"

    def __init__(self, item_dict):
        super().__init__(item_dict)

@op_register_item_type
class OPDatabaseItem(OPAbstractItem):
    CATEGORY = "DATABASE"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def type(self) -> str:
        return self.field_value_by_id("type")

    @property
    def server(self) -> str:
        return self.field_value_by_id("server")

    @property
    def port(self) -> int:
        return self.field_value_by_id("port")

    @property
    def database(self) -> str:
        return self.field_value_by_id("database")

    @property
    def username(self) -> str:
        return self.field_value_by_id("username")

    @property
    def password(self) -> str:
        return self.field_value_by_id("password")
