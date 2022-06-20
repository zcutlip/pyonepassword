from datetime import date

from .expected_item import ExpectedItemBase, ExpectedItemData


class ExpectedAPICredential(ExpectedItemBase):
    """
    "Example API Credential":
        {
            "id": "jgou2ypa4ceurm4fetya3kptau",
            "title": "Example API Credential",
            "category": "API_CREDENTIAL",
            "last_edited_by": "5GHHPJK5HZC5BAT7WDUXW57G44",
            "created_at": "2022-05-04T01:08:14Z",
            "updated_at": "2022-05-04T01:09:50Z",
            "additional_information": "other",
            "notes": null,
            "username": "__token__",
            "credential": "212784acd95ae1d67e8d513602e7b5acf60dbb0c811d9628a23151aafade72b5",
            "type": "other",
            "filename": null,
            "valid_from": 1641038460,
            "expires": 1656590460,
            "hostname": "api.example.com"
        }
    """

    @property
    def unique_id(self) -> str:
        return self._data["id"]

    @property
    def title(self) -> str:
        return self._data["title"]

    @property
    def username(self) -> str:
        return self._data["username"]

    @property
    def credential(self) -> str:
        return self._data["credential"]

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def filename(self) -> str:
        return self._data["filename"]

    @property
    def valid_from(self) -> date:
        timestamp = self._data["valid_from"]
        valid_from = date.fromtimestamp(timestamp)
        return valid_from

    @property
    def expires(self) -> date:
        timestamp = self._data["expires"]
        expires = date.fromtimestamp(timestamp)
        return expires

    @property
    def hostname(self) -> str:
        return self._data["hostname"]


class ExpectedAPICredentialData(ExpectedItemData):

    def api_cred_data_for_login(self, login_identifier):
        item_dict = self._data[login_identifier]
        login_item = ExpectedAPICredential(item_dict)
        return login_item
