from .expected_item import ExpectedItemBase, ExpectedItemData

"""
"Example SSH Key": {
            "id": "k7t4uzbuf3fn7d7wrajh5xb3gi",
            "title": "Example SSH Key",
            "category": "SSH_KEY",
            "last_edited_by": "5GHHPJK5HZC5BAT7WDUXW57G44",
            "created_at": "2022-06-20T21:06:07Z",
            "updated_at": "2022-06-21T18:41:55Z",
            "additional_information": "SHA256:O+ehRdAhXz8+PGBCU0u4hOv/aHV9in9aMLPxWO2JsFA",
            "notes": null,
            "public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILpE4IxrziuKMe/PNV1BheNOSDP3M4++aynx1+7iHIHI",
            "public_key_ref": "op://Test Data/Example SSH Key/public key",
            "fingerprint": "SHA256:O+ehRdAhXz8+PGBCU0u4hOv/aHV9in9aMLPxWO2JsFA",
            "fingerprint_ref": "op://Test Data/Example SSH Key/fingerprint",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMFMCAQEwBQYDK2VwBCIEIKfpg35IQovbLROU0bzSWZNPjfhSuTuK9RV/pMYNb3ZK\noSMDIQC6ROCMa84rijHvzzVdQYXjTkgz9zOPvmsp8dfu4hyByA==\n-----END PRIVATE KEY-----\n",
            "private_key_ref": "op://Test Data/Example SSH Key/private key",
            "key_type": "ed25519",
            "key_type_ref": "op://Test Data/Example SSH Key/key type"
        }
"""


class ExpectedSSHKey(ExpectedItemBase):

    @property
    def public_key(self) -> str:
        return self._data["public_key"]

    @property
    def public_key_ref(self) -> str:
        return self._data["public_key_ref"]

    @property
    def fingerprint(self) -> str:
        return self._data["fingerprint"]

    @property
    def fingerprint_ref(self) -> str:
        return self._data["fingerprint_ref"]

    @property
    def private_key(self) -> str:
        return self._data["private_key"]

    @property
    def private_key_ref(self) -> str:
        return self._data["private_key_ref"]

    @property
    def key_type(self) -> str:
        return self._data["key_type"]

    @property
    def key_type_ref(self) -> str:
        return self._data["key_type_ref"]


class ExpectedSSHKeyData(ExpectedItemData):

    def data_for_ssh_key(self, ssh_key_identifier):
        item_dict = self.data_for_name(ssh_key_identifier)
        ssh_key_item = ExpectedSSHKey(item_dict)
        return ssh_key_item
