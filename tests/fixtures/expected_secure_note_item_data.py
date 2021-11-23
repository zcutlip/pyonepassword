from .expected_item import ExpectedItemBase


class ExpectedSecureNoteItem(ExpectedItemBase):

    @property
    def note_text(self) -> str:
        return self._data["notesPlain"]
