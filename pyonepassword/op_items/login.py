import copy

from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem, item_template, OPItemOverview

@op_register_item_type
class OPLoginItem(OPAbstractItem):
    TEMPLATE_ID = "001"
    ITEM_CATEGORY = "Login"

    class _OPLoginItemOverview(OPItemOverview):
        class _URLEntry(dict):
            def __init__(self, url_dict):
                ud = copy.deepcopy(url_dict)
                super().__init__(ud)

            @property
            def label(self):
                return self["l"]

            @property
            def url(self):
                return self["u"]

        def __init__(self, overview_dict):
            super().__init__(overview_dict)
            _urls = self._process_urls()
            if _urls is not None:
                self["URLs"] = _urls

        def _process_urls(self):
            url_items = None
            url_dicts = self.get("URLs", [])
            if url_dicts:
                url_items = []
                for d in url_dicts:
                    url = self._URLEntry(d)
                    url_items.append(url)
            return url_items

        def url_list(self):
            return self.get("URLs", [])

    def __init__(self, item_dict, **kwargs):
        super().__init__(item_dict, **kwargs)

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

@item_template
class OPLoginItemTemplate(OPLoginItem):
    def __init__(self,  username, password, *args, url=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password
        self.url = url
