from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem


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
