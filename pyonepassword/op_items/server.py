from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem


@op_register_item_type
class OPServerItem(OPAbstractItem):
    TEMPLATE_ID = "110"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def password(self):
        password = self.primary_section_field_value("password")
        return password

    @property
    def username(self):
        username = self.primary_section_field_value("username")
        return username

    @property
    def url(self):
        url = self.primary_section_field_value("URL")
        return url

    @property
    def admin_console_password(self):
        password = self.field_value_by_section_title(
            "Admin Console", "console password")
        return password

    @property
    def admin_console_username(self):
        username = self.field_value_by_section_title("admin console username")
        return username

    @property
    def admin_console_url(self):
        url = self.field_value_by_section_title(
            "Admin Console", "admin console URL")
        return url
