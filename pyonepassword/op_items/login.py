from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem

@op_register_item_type
class OPLoginItem(OPAbstractItem):
    TEMPLATE_ID = "001"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @classmethod
    def from_template(cls, username, password):
        obj: OPLoginItem = super().from_template()
        obj.username = username
        obj.password = password
        return obj

    def get_item_field(self, field_designation):
        details = self._item_dict["details"]
        fields = details["fields"]
        field = None
        for f in fields:
            if f["designation"] == field_designation:
                field = f
                break
        return field

    def get_item_field_value(self, field_designation):
        field_value = None
        field = self.get_item_field(field_designation)
        field_value = field["value"]
        return field_value

    @property
    def username(self):
        username = self.get_item_field_value("username")
        return username

    @username.setter
    def username(self, username: str):
        username_field = self.get_item_field("username")
        username_field["value"] = username

    @property
    def password(self):
        password = self.get_item_field_value("password")
        return password

    @password.setter
    def password(self, password: str):
        password_field = self.get_item_field("password")
        password_field["value"] = password
