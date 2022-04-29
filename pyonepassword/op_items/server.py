from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem, OPItemTemplateMixin


@op_register_item_descriptor_type
class OPServerItemDescriptor(OPAbstractItemDescriptor):
    CATEGORY = "SERVER"

    def __init__(self, item_dict):
        super().__init__(item_dict)


@op_register_item_type
class OPServerItem(OPAbstractItem):
    CATEGORY = "SERVER"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def password(self):
        password = self.field_value_by_id("password")
        return password

    @password.setter
    def password(self, password: str):
        self.set_primary_section_field_value("password", password)

    @property
    def username(self):
        username = self.field_value_by_id("username")
        return username

    @username.setter
    def username(self, username: str):
        self.set_primary_section_field_value("username", username)

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


class OPServerItemTemplate(OPItemTemplateMixin, OPServerItem):
    TEMPLATE_ID = OPServerItem.TEMPLATE_ID
    ITEM_CATEGORY = "Server"

    def __init__(self, username, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password
