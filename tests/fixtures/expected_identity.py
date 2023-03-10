from .expected_item import ExpectedItemBase, ExpectedItemData


class ExpectedIdenity(ExpectedItemBase):

    def __init__(self, item_dict):
        super().__init__(item_dict)


class ExpectedIdenityItemData(ExpectedItemData):

    def data_for_identity(self, identity_identifier):
        item_dict = self.data_for_name(identity_identifier)
        identity_item = ExpectedIdenity(item_dict)
        return identity_item
