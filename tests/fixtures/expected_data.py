from typing import Dict, List

from .paths import EXPECTED_DATA_PATH, EXPECTED_DATA_REGISTRY_PATH
from .valid_data import ValidData


class ExpectedData(ValidData):
    REGISTRY_PATH = EXPECTED_DATA_REGISTRY_PATH
    DATA_PATH = EXPECTED_DATA_PATH

    def lookup_item(self, item_id):
        item_data = self.item_data
        item = item_data[item_id]
        return item

    def lookup_document(self, document_id):
        document_data = self.document_data
        doc_dict = document_data[document_id]
        return doc_dict

    def lookup_vault(self, vault_id):
        vault_data = self.vault_data
        vault_dict = vault_data[vault_id]
        return vault_dict

    def lookup_user(self, user_id):
        user_data = self.user_data
        user_dict = user_data[user_id]
        return user_dict

    @property
    def item_data(self) -> Dict[str, Dict]:
        data = self.data_for_name("expected-item-data")
        return data

    @property
    def document_data(self) -> Dict[str, Dict]:
        data = self.data_for_name("expected-document-data")
        return data

    @property
    def vault_data(self) -> Dict[str, Dict]:
        data = self.data_for_name("expected-vault-data")
        return data

    @property
    def vault_list_data(self) -> Dict[str, List]:
        data = self.data_for_name("expected-vault-list-data")
        return data

    @property
    def user_data(self) -> Dict[str, Dict]:
        data = self.data_for_name("expected-user-data")
        return data

    @property
    def user_list_data(self) -> Dict[str, List]:
        data = self.data_for_name("expected-user-list-data")
        return data

    @property
    def group_data(self) -> Dict[str, Dict]:
        data = self.data_for_name("expected-group-data")
        return data

    @property
    def group_list_data(self) -> Dict[str, List]:
        data = self.data_for_name("expected-group-list-data")
        return data

    @property
    def account_data(self) -> Dict[str, Dict]:
        data = self.data_for_name("expected-account-data")
        return data

    @property
    def item_fields(self) -> Dict[str, Dict]:
        data = self.data_for_name("expected-item-field-data")
        return data

    @property
    def op_config_data(self) -> Dict[str, Dict]:
        data = self.data_for_name("expected-op-config-data")
        return data

    @property
    def datetime_data(self) -> Dict[str, str]:
        data = self.data_for_name("expected-datetime-data")
        return data

    @property
    def misc_data(self) -> Dict[str, str]:
        data = self.data_for_name("expected-misc-data")
        return data
