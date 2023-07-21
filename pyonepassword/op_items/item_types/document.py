from .._item_descriptor_registry import op_register_item_descriptor_type
from .._item_type_registry import op_register_item_type
from ._item_base import OPAbstractItem
from ._item_descriptor_base import OPAbstractItemDescriptor


@op_register_item_descriptor_type
class OPDocumentItemDescriptor(OPAbstractItemDescriptor):
    CATEGORY = "DOCUMENT"

    def __init__(self, item_dict):
        super().__init__(item_dict)


@op_register_item_type
class OPDocumentItem(OPAbstractItem):
    CATEGORY = "DOCUMENT"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def file_name(self):
        first_file = self.files[0]
        file_name = first_file.name
        return file_name


@op_register_item_type
class OPDocumentItemRelaxedValidation(OPDocumentItem):
    _relaxed_validation = True
