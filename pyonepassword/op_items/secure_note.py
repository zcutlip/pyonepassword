from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem

# {
#     "uuid": "zjc6s5ri3rhcxploofa67jamze",
#     "templateUuid": "003",
#     "trashed": "N",
#     "createdAt": "2021-03-19T23:27:12Z",
#     "updatedAt": "2021-03-19T23:30:10Z",
#     "changerUuid": "5GHHPJK5HZC5BAT7WDUXW57G44",
#     "itemVersion": 2,
#     "vaultUuid": "gshlsjsajnawtnjynzgwmiebge",
#     "details": {
#         "notesPlain": "Note text here. **Mardown** supported.\n\nWhat does the note text look like?",
#         "passwordHistory": [],
#         "sections": [
#             {
#                 "name": "linked items",
#                 "title": "Related Items"
#             }
#         ]
#     },
#     "overview": {
#         "ainfo": "Note text here. **Mardown** supported.",
#         "ps": 0,
#         "title": "Example Secure Note"
#     }
# }


@op_register_item_descriptor_type
class OPSecureNoteItemDescriptor(OPAbstractItemDescriptor):
    CATEGORY = "SECURE_NOTE"

    def __init__(self, item_dict):
        super().__init__(item_dict)


@op_register_item_type
class OPSecureNoteItem(OPAbstractItem):
    CATEGORY = "SECURE_NOTE"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def note_text(self):
        text = self.field_value_by_id("notesPlain")
        return text
