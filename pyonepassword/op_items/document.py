from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem


class OPDocumentFile(dict):
    def __init__(self, file_dict):
        super().__init__(file_dict)

    @property
    def file_id(self) -> str:
        return self["id"]

    @property
    def name(self) -> str:
        return self["name"]

    @property
    def size(self) -> int:
        return self["size"]

    @property
    def content_path(self) -> str:
        return self["content_path"]


@op_register_item_descriptor_type
class OPDocumentItemDescriptor(OPAbstractItemDescriptor):
    TEMPLATE_ID = "006"

    def __init__(self, item_dict):
        super().__init__(item_dict)


@op_register_item_type
class OPDocumentItem(OPAbstractItem):
    TEMPLATE_ID = "006"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def file_name(self):
        details = self._item_dict["details"]
        document_attributes = details["documentAttributes"]
        file_name = document_attributes["fileName"]
        return file_name
