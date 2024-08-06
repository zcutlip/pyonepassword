from typing import List, Optional

from pyonepassword import OP  # noqa: F401
from pyonepassword.api.object_types import (
    OPItemField,
    OPLoginItemTemplate,
    OPNewStringField,
    OPPasswordRecipe,
    OPSection,
    OPSecureNoteItem
)
from pyonepassword.op_items._new_item import OPNewItemMixin

username = "test_username"
title = "Test Login Item"

recipe = OPPasswordRecipe(length=40, digits=False, symbols=False)
new_item_1 = OPLoginItemTemplate(title, username)


class OPNewSecureNoteItem(OPNewItemMixin, OPSecureNoteItem):

    def __init__(self,
                 title: str,
                 note_text: str,
                 fields: Optional[List[OPItemField]] = None,
                 sections: Optional[List[OPSection]] = None):

        if sections is None:  # pragma: no coverage
            sections = []
        else:
            sections = list(sections)
        if fields is None:  # pragma: no coverage
            fields = []
        else:
            fields = list(fields)

        note_text_field = OPNewStringField(
            "notesPlain",
            note_text,
            field_id="notesPlain")

        fields.append(note_text_field)

        super().__init__(title, sections=sections, fields=fields)
