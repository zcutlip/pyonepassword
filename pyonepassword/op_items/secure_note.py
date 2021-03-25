from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem


@op_register_item_type
class OPSecureNoteItem(OPAbstractItem):
    TEMPLATE_ID = "003"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def note_text(self):
        text = self.get_item_field_value("notesPlain")
        return text
