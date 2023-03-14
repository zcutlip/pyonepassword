import json
from typing import List, Union

from ..json import safe_unjson
from ._item_descriptor_registry import OPItemDescriptorFactory
from .item_types._item_descriptor_base import OPAbstractItemDescriptor


class OPItemList(List[OPAbstractItemDescriptor]):
    def __init__(self, item_list_json: Union[str, List], generic_okay=False):
        super().__init__()
        item_list = safe_unjson(item_list_json)
        for i_dict in item_list:
            descriptor = OPItemDescriptorFactory.item_descriptor(
                i_dict, generic_okay=generic_okay)
            self.append(descriptor)

        # 'op item list' returns items in a non-deterministic order
        # so sorting ourselves hopefully ensures we are in a consistent order every time
        # this will mainly make it easier for testing
        # so multiple queries for the same list of items will yield the same result
        self.sort()

    def serialize(self, indent=None) -> str:
        json_str = json.dumps(self, indent=indent)
        return json_str

    def sort(self):
        # we really want to be sorted by title, since that's the most
        # human friendly (mainly for troubleshooting)
        # but in the case if title collisions, this is still non-deterministic
        # since 'op' may return them in a non-deterministic order
        # since list.sort() is considered stable we can ensure items
        # with the same title are in a particular order relative to each other by...
        # first, sorting by unique id
        super().sort(key=lambda item: item.unique_id)
        # Then sort by title
        super().sort(key=lambda item: item.title)
