from .expected_data import ExpectedData


class ExpectedConfigAccount:
    def __init__(self, config_account_dict):
        self._data = config_account_dict

    @property
    def shorthand(self) -> str:
        return self._data["shorthand"]

    @property
    def account_uuid(self) -> str:
        return self._data["accountUUID"]

    @property
    def url(self) -> str:
        return self._data["url"]

    @property
    def email(self) -> str:
        return self._data['email']

    @property
    def user_uuid(self) -> str:
        return self._data["userUUID"]


class ExpectedConfigData:
    def __init__(self):
        expected_data = ExpectedData()
        self._data = expected_data.op_config_data

    def data_for_key(self, key: str) -> ExpectedConfigAccount:
        data = self._data[key]
        data = ExpectedConfigAccount(data)
        return data
