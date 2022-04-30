from .expected_item import ExpectedItemBase, ExpectedItemData


class ExampleLogin(ExpectedItemBase):

    @property
    def username(self) -> str:
        return self._data["username"]

    @property
    def password(self) -> str:
        return self._data["password"]


class ExpectedLoginItemData(ExpectedItemData):

    def data_for_login(self, note_identifier):
        item_dict = self._data[note_identifier]
        login_item = ExampleLogin(item_dict)
        return login_item
