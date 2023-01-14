from typing import List, Union

from ..json import safe_unjson
from ..json import safe_unjson
from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import OPItemDescriptorFactory


class OPItemList(List[OPAbstractItemDescriptor]):
    def __init__(self, item_list_json: Union[Union[str, List], List], generic_okay=False):
        super().__init__()
        item_list = safe_unjson(item_list_json)
        for i_dict in item_list:
            descriptor = OPItemDescriptorFactory.item_descriptor(
                i_dict, generic_okay=generic_okay)
            self.append(descriptor)
