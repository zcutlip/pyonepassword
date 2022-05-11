from typing import Dict

from .expected_data import ExpectedData


class ExpectedVault:
    def __init__(self, vault_dict: Dict):
        self._data = vault_dict

    @property
    def unique_id(self) -> str:
        return self._data["unique_id"]

    @property
    def description(self) -> str:
        return self._data["description"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def returncode(self) -> int:
        return self._data["returncode"]


class ExpectedVaultData:
    def __init__(self):
        expected_data = ExpectedData()
        vault_data: Dict = expected_data.vault_data
        self._data: Dict = vault_data

    def data_for_vault(self, vault_identifier: str):
        vault_dict = self._data[vault_identifier]
        user = ExpectedVault(vault_dict)
        return user


class ExpectedVaultListEntry:
    def __init__(self, user_item: Dict) -> None:
        self._data = user_item

    @property
    def unique_id(self) -> str:
        return self._data["unique_id"]

    @property
    def name(self) -> str:
        return self._data["name"]


class ExpectedVaultListData:

    def __init__(self) -> None:
        expected_data = ExpectedData()
        vault_list_data: Dict = expected_data.vault_list_data
        self._data: Dict = vault_list_data

    def data_for_key(self, data_key: str):
        vault_list = self._data[data_key]
        vault_list = [ExpectedVaultListEntry(entry_dict)
                      for entry_dict in vault_list]
        return vault_list
