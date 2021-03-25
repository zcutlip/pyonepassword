from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem

@op_register_item_type
class OPLoginItem(OPAbstractItem):
    TEMPLATE_ID = "001"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    def get_item_field_value(self, field_designation):
        field_value = None
        details = self._item_dict["details"]
        fields = details["fields"]
        for f in fields:
            if f["designation"] == field_designation:
                field_value = f["value"]
                break
        return field_value

    @property
    def username(self):
        username = None
        details = self._item_dict["details"]
        fields = details["fields"]
        for f in fields:
            if f["designation"] == "username":
                username = f["value"]
                break

        return username

    @property
    def password(self):
        password = self.get_item_field_value("password")
        return password
