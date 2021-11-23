from .expected_item import ExpectedItemBase, ExpectedItemData


class ExpectedItemPassword(ExpectedItemBase):

    @property
    def password(self) -> str:
        return self._data["password"]


class ExpectedPasswordItemData(ExpectedItemData):

    def data_for_password(self, password_identifier: str):
        item_dict = self._data[password_identifier]
        password_item = ExpectedItemPassword(item_dict)
        return password_item
