"""
Miscellaneous classes for objects return by 'op get' other than item or document objects
"""
import json
from datetime import datetime
from json.decoder import JSONDecodeError
from typing import Union

from .py_op_exceptions import _OPAbstractException
from ._datetime import fromisoformat_z


class OPInvalidObjectException(_OPAbstractException):
    def __init__(self, msg, object_json):
        super().__init__(msg)
        self.object_json = object_json


class OPInvalidUserException(OPInvalidObjectException):
    def __init__(self, msg, user_json):
        super().__init__(msg, user_json)


class OPUser(dict):
    def __init__(self, user_dict_or_json: Union[str, dict]):
        if isinstance(user_dict_or_json, str):
            try:
                user_dict = json.loads(user_dict_or_json)
            except JSONDecodeError as jdce:
                raise OPInvalidUserException(
                    f"Failed to unserialize user json: {jdce}", user_dict_or_json)
        else:
            user_dict = user_dict_or_json
        super().__init__(user_dict)

    @property
    def uuid(self):
        return self["uuid"]

    @property
    def created_at(self) -> datetime:
        created = self["createdAt"]
        created = fromisoformat_z(created)
        return created

    @property
    def updatedAt(self) -> datetime:
        updated = self["updatedAt"]
        updated = fromisoformat_z(updated)
        return updated

    @property
    def last_auth_at(self) -> datetime:
        last_auth = self["updatedAt"]
        last_auth = fromisoformat_z(last_auth)
        return last_auth

    @property
    def email(self) -> str:
        return self["email"]

    @property
    def first_name(self) -> str:
        return self["firstName"]

    @property
    def last_name(self) -> str:
        return self["lastName"]

    @property
    def name(self) -> str:
        return self["name"]

    @property
    def attr_version(self) -> int:
        return self["attrVersion"]

    @property
    def keyset_version(self) -> int:
        return self["keysetVersion"]

    @property
    def state(self) -> str:
        return self["state"]

    @property
    def type(self) -> str:
        return self["type"]

    @property
    def avatar(self) -> str:
        return self["avatar"]

    @property
    def language(self) -> str:
        return self["language"]

    @property
    def account_key_format(self) -> str:
        return self["accountKeyFormat"]

    @property
    def account_key_uuid(self) -> str:
        return self["accountKeyUuid"]

    @property
    def combined_permissions(self) -> str:
        return self["combinedPermissions"]
