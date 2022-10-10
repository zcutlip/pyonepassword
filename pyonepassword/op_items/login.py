from typing import List

from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type
from ._new_fields import OPNewPasswordField, OPNewUsernameField
from ._new_item import OPNewItemMixin
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem


class OPNewLoginItemURLException(Exception):
    pass


@op_register_item_descriptor_type
class OPLoginDescriptorItem(OPAbstractItemDescriptor):
    CATEGORY = "LOGIN"

    def __init__(self, item_dict):
        super().__init__(item_dict)


class OPLoginItemURL(dict):
    def __init__(self, url_dict):
        super().__init__(url_dict)

    @property
    def label(self) -> str:
        return self.get("label")

    @property
    def primary(self) -> bool:
        primary = self.get("primary", False)
        return primary

    @property
    def href(self) -> str:
        return self["href"]


class OPLoginItemNewURL(OPLoginItemURL):
    def __init__(self, url: str, label: str, primary: bool = False):
        url_dict = {
            "label": label,
            "primary": primary,
            "href": url
        }
        super().__init__(url_dict)


class OPLoginItemNewPrimaryURL(OPLoginItemNewURL):
    def __init__(self, url: str, label: str):
        super().__init__(url, label, primary=True)


@op_register_item_type
class OPLoginItem(OPAbstractItem):
    CATEGORY = "LOGIN"

    def __init__(self, item_dict_or_json):
        super().__init__(item_dict_or_json)
        urls = []
        primary_url = None
        url_list = self.get("urls", [])
        for url_dict in url_list:
            url = OPLoginItemURL(url_dict)
            if url.primary:
                primary_url = url
            urls.append(url)
        self._urls = urls
        self._primary_url = primary_url

    @property
    def username(self):
        username = self.field_value_by_id("username")
        return username

    @property
    def password(self):
        password = self.field_value_by_id("password")
        return password

    @property
    def urls(self) -> List[OPLoginItemURL]:
        return self._urls

    @property
    def primary_url(self) -> OPLoginItemURL:
        return self._primary_url


class OPNewLoginItem(OPNewItemMixin, OPLoginItem):
    FIELD_ID_USERNAME = "username"
    FIELD_ID_PASSWORD = "password"

    def __init__(self,
                 title: str,
                 username: str,
                 password: str = None,
                 url: OPLoginItemURL = None):

        # were we provided a URL string intead of a OPLoginItemURL object?
        # We can't just create an object because we don't know what the label should be
        # TODO: should we just apply a standard primary URL label, like "website"?
        if url is not None and not isinstance(url, OPLoginItemURL):
            raise OPNewLoginItemURLException(
                "URL must be in instance of OPLoginItemURL. Create a new one with OPLoginItemNewURL, or OPLoginItemNewPrimaryURL")

        username_field = OPNewUsernameField(
            self.FIELD_ID_USERNAME,
            username,
            field_id=self.FIELD_ID_USERNAME
        )

        password_field = OPNewPasswordField(
            self.FIELD_ID_PASSWORD,
            password,
            field_id=self.FIELD_ID_PASSWORD
        )
        fields = [username_field, password_field]
        urls = []
        if url:
            urls.append(url)
        extra_data = {"urls": urls}
        super().__init__(title, fields=fields, extra_data=extra_data)

    def add_url(self, url: OPLoginItemURL):
        has_primary = False
        if self.primary_url:
            has_primary = True
        if url.primary and has_primary:
            raise OPNewLoginItemURLException("Can't add multiple primary URLs")

        self._urls.append(url)
        if url.primary:
            self._primary_url = url
