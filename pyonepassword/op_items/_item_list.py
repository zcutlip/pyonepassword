import json
from typing import List

from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import OPItemDescriptorFactory


class OPItemList(List[OPAbstractItemDescriptor]):
    def __init__(self, item_list_json: str):
        super().__init__()
        item_list = json.loads(item_list_json)
        for i_dict in item_list:
            descriptor = OPItemDescriptorFactory.item_descriptor(i_dict)
            self.append(descriptor)
