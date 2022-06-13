from typing import List

from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem


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
