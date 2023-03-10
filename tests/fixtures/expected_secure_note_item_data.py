from .expected_item import ExpectedItemBase, ExpectedItemData


class ExpectedSecureNoteItem(ExpectedItemBase):

    @property
    def note_text(self) -> str:
        return self._data["notesPlain"]


class ExpectedSecureNoteItemData(ExpectedItemData):

    def data_for_note(self, note_identifier):
        item_dict = self.data_for_name(note_identifier)
        note_item = ExpectedSecureNoteItem(item_dict)
        return note_item
