from .expected_item import ExpectedItemBase, ExpectedItemData


class ExpectedDatabaseItem(ExpectedItemBase):

    @property
    def username(self) -> str:
        field = self.field_by_id("username")
        return field.value

    @property
    def password(self) -> str:
        field = self.field_by_id("password")
        return field.value

    @property
    def database_type(self) -> str:
        field = self.field_by_id("database_type")
        return field.value

    @property
    def hostname(self) -> str:
        field = self.field_by_id("hostname")
        return field.value

    @property
    def port(self) -> str:
        # port is a string even though it's (typicaly?) numerical
        # 1password will accept arbitrary strings here
        field = self.field_by_id("port")
        return field.value

    @property
    def database(self) -> str:
        field = self.field_by_id("database")
        return field.value

    @property
    def sid(self) -> str:
        field = self.field_by_id("sid")
        return field.value

    @property
    def alias(self) -> str:
        field = self.field_by_id("alias")
        return field.value

    @property
    def options(self) -> str:
        field = self.field_by_id("options")
        return field.value


class ExpectedDatabaseItemData(ExpectedItemData):

    def data_for_database(self, database_identifier) -> ExpectedDatabaseItem:
        item_dict = self.data_for_name(database_identifier)
        login_item = ExpectedDatabaseItem(item_dict)
        return login_item
