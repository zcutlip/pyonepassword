from typing import Dict

from .expected_data import ExpectedData


class ExpectedVault:
    def __init__(self, vault_dict: Dict):
        self._data = vault_dict

    @property
    def uuid(self) -> str:
        return self._data["uuid"]

    @property
    def desc(self) -> str:
        return self._data["desc"]

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
