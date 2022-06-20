import datetime

from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem


@op_register_item_descriptor_type
class OPAPICredentialItemDescriptor(OPAbstractItemDescriptor):
    CATEGORY = "API_CREDENTIAL"

    def __init__(self, item_dict):
        super().__init__(item_dict)


"""
{
  "id": "jgou2ypa4ceurm4fetya3kptau",
  "title": "Example API Credential",
  "version": 3,
  "vault": {
    "id": "gshlsjsajnawtnjynzgwmiebge",
    "name": "Test Data"
  },
  "category": "API_CREDENTIAL",
  "last_edited_by": "5GHHPJK5HZC5BAT7WDUXW57G44",
  "created_at": "2022-05-04T01:08:14Z",
  "updated_at": "2022-05-04T01:09:50Z",
  "additional_information": "other",
  "fields": [
    {
      "id": "notesPlain",
      "type": "STRING",
      "purpose": "NOTES",
      "label": "notesPlain",
      "reference": "op://Test Data/Example API Credential/notesPlain"
    },
    {
      "id": "username",
      "type": "STRING",
      "label": "username",
      "value": "__token__",
      "reference": "op://Test Data/Example API Credential/username"
    },
    {
      "id": "credential",
      "type": "CONCEALED",
      "label": "credential",
      "value": "212784acd95ae1d67e8d513602e7b5acf60dbb0c811d9628a23151aafade72b5",
      "reference": "op://Test Data/Example API Credential/credential"
    },
    {
      "id": "type",
      "type": "MENU",
      "label": "type",
      "value": "other",
      "reference": "op://Test Data/Example API Credential/type"
    },
    {
      "id": "filename",
      "type": "STRING",
      "label": "filename",
      "reference": "op://Test Data/Example API Credential/filename"
    },
    {
      "id": "validFrom",
      "type": "DATE",
      "label": "valid from",
      "value": "1641038460",
      "reference": "op://Test Data/Example API Credential/valid from"
    },
    {
      "id": "expires",
      "type": "DATE",
      "label": "expires",
      "value": "1656590460",
      "reference": "op://Test Data/Example API Credential/expires"
    },
    {
      "id": "hostname",
      "type": "STRING",
      "label": "hostname",
      "value": "api.example.com",
      "reference": "op://Test Data/Example API Credential/hostname"
    }
  ]
}
"""


@op_register_item_type
class OPAPICredentialItem(OPAbstractItem):
    CATEGORY = "API_CREDENTIAL"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def username(self):
        username = self.field_value_by_id("username")
        return username

    @property
    def credential(self) -> str:
        cred = self.field_value_by_id("credential")
        return cred

    @property
    def type(self) -> str:
        return self.field_value_by_id("type")

    @property
    def filename(self) -> str:
        return self.field_value_by_id("filename")

    @property
    def valid_from(self) -> datetime.date:
        valid_from = self.field_value_by_id("validFrom")
        valid_from = int(valid_from)
        valid_from = datetime.date.fromtimestamp(valid_from)
        return valid_from

    @property
    def expires(self) -> datetime.date:
        expires = self.field_value_by_id("expires")
        expires = int(expires)
        expires = datetime.date.fromtimestamp(expires)
        return expires

    @property
    def hostname(self) -> str:
        return self.field_value_by_id("hostname")
