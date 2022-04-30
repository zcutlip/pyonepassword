from typing import Dict

from .expected_item import ExpectedItemBase, ExpectedItemData


class ExpectedServerSSHKeys:

    def __init__(self, key_dict: Dict[str, str]):
        self._data = key_dict

    @property
    def pubkey_digest(self) -> str:
        return self._data["pubkey_digest"]

    @property
    def pivkey_digest(self) -> str:
        return self._data["privkey_digest"]

    @property
    def passphrase(self) -> str:
        return self._data["passphrase"]


class ExpectedServer(ExpectedItemBase):
    """
    Example Server":{
            "unique_id": "hqnf5vpzc5mg4x4asrpbvoi54u",
            "title": "Example Server",
            "username": "admin",
            "password": "example_admin_password",
            "created_at": "2021-06-29T18:31:30Z",
            "updated_at": "2021-06-29T18:31:30Z",
            "ssh_keys":{
                "id_ed25519":{
                    "pubkey_digest":"83312cfb5a2d9bb6bb90e89b73c48554df964ef3b29021e66ffa2ffbda649ac4",
                    "privkey_digest":"78670118cc184cf45d0fee82bcac4c3a0d2528dd4aa5b8406ee4a059133efa2a",
                    "passphrase": "example_ssh_key_password"
                }
            }
        },
    """

    @property
    def username(self) -> str:
        return self._data["username"]

    @property
    def password(self) -> str:
        return self._data["password"]

    @property
    def ssh_keys(self) -> Dict[str, Dict[str, str]]:
        return self._data["ssh_keys"]

    def ssh_keys_for_id(self, ssh_key_id) -> ExpectedServerSSHKeys:
        all_keys = self.ssh_keys
        key_dict = all_keys[ssh_key_id]
        key_obj = ExpectedServerSSHKeys(key_dict)
        return key_obj


class ExpectedServerItemData(ExpectedItemData):

    def data_for_server(self, note_identifier):
        item_dict = self._data[note_identifier]
        server_item = ExpectedServer(item_dict)
        return server_item
