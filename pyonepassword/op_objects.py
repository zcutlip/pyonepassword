"""
Miscellaneous classes for objects return by 'op get' other than item or document objects
"""
import json
from abc import ABCMeta, abstractmethod
from datetime import datetime
from json.decoder import JSONDecodeError
from typing import Dict, List, TypeVar, Union

from ._datetime import fromisoformat_z
from .json import safe_unjson
from .py_op_exceptions import _OPAbstractException


class OPInvalidObjectException(_OPAbstractException):
    """
    The data provided to generate an OP query object failed to parse or validate

    Attributes
    ----------
    object_json : Union[str, None]
        The original JSON from the 'op' command query, if available
    """

    def __init__(self, msg, object_json):
        super().__init__(msg)
        self.object_json = object_json


class OPInvalidUserException(OPInvalidObjectException):
    """
    The data provided to generate an 'op get user' query object failed to parse or validate
    """
    pass


class OPInvalidGroupException(OPInvalidObjectException):
    """
    The data provided to from 'op get group' failed to parse or validate
    """
    pass


class OPInvalidUserListException(OPInvalidObjectException):
    """
    The data provided from 'op list users' failed to parse or validate
    """
    pass


class OPInvalidGroupListException(OPInvalidObjectException):
    """
    The data provided from 'op list groups' failed to parse or validate
    """
    pass


class OPInvalidVaultException(OPInvalidObjectException):
    """
    The data provided from 'op get vault' failed to parse or validate
    """
    pass


class OPInvalidVaultListException(OPInvalidGroupListException):
    """
    The data provided from 'op list vaults' failed to parse or validate
    """


DT = TypeVar('DT')


class _OPDescriptorList(List[DT]):
    """
    A class for type-hinting lists of 1Password object descriptors
    """
    pass


class OPAbstractObject(dict, metaclass=ABCMeta):
    """
    Abstract base class for 1Password objects as returned by 'op list|get <object class>'
    """

    @abstractmethod
    def __init__(self, dict_or_json: Union[str, dict]):
        obj_dict = safe_unjson(dict_or_json)
        super().__init__(obj_dict)

    @property
    def unique_id(self):
        """
        str: The object's "id" field
        """
        return self["id"]

    @property
    def name(self) -> str:
        """
        str : The name attribute
        """
        return self["name"]


class OPBaseObject(OPAbstractObject):
    """
    Base class for miscellaneous 1Password objects as returned by 'op get <object class>'
    """

    @property
    def created_at(self) -> datetime:
        """
        datetime : The created_at attribute parsed as a datetime object
        """
        created = self["created_at"]
        created = fromisoformat_z(created)
        return created

    @property
    def updated_at(self) -> datetime:
        """
        datetime : The updated_at attribute parsed as a datetime object
        """
        updated = self["updated_at"]
        updated = fromisoformat_z(updated)
        return updated


class OPUser(OPBaseObject):
    """
    A dictionary of full details about a 1Password user.
    This can be treated as a normal dictionary. In addition, it has a convenience
    property for each key in the the dictionary.

    Note
    ----
    Date-related properties return parsed 'datetime' objects. To access the original
    date strings, use the corresponding dictionary key.
    """

    def __init__(self, user_dict_or_json: Union[str, dict]):
        """
        Parameters
        ----------
        user_dict_or_json : Union[str, dict]
            A dictionary or JSON string return from 'op get user'. If a JSON string is provided,
            it will first be unserialized to a dict object.

        Raises
        ------
        OPInvalidUserException
            If JSON is provided and unserializing fails.

        """
        try:
            super().__init__(user_dict_or_json)
        except JSONDecodeError as jdce:
            raise OPInvalidUserException(
                f"Failed to unserialize user json: {jdce}", user_dict_or_json) from jdce

    @property
    def email(self) -> str:
        """
        str : The email attribute
        """
        return self["email"]

    @property
    def type(self) -> str:
        """
        str : The type attribute
        """
        return self["type"]

    @property
    def state(self) -> str:
        """
        str : The state attribute
        """
        return self["state"]

    @property
    def last_auth_at(self) -> datetime:
        """
        datetime : The lastAuthAt attribute parsed as a datetime object
        """
        last_auth = self["last_auth_at"]
        last_auth = fromisoformat_z(last_auth)
        return last_auth


class OPGroup(OPBaseObject):
    """
    A dictionary of full details about a 1Password group.
    This can be treated as a normal dictionary. In addition, it has a convenience
    property for each key in the the dictionary.

    Note
    ----
    Date-related properties return parsed 'datetime' objects. To access the original
    date strings, use the corresponding dictionary key.
    """

    def __init__(self, group_dict_or_json: Union[str, dict]):
        """
        Parameters
        ----------
        user_dict_or_json : Union[str, dict]
            A dictionary or JSON string return from 'op get user'. If a JSON string is provided,
            it will first be unserialized to a dict object.

        Raises
        ------
        OPInvalidGroupException
            If JSON is provided and unserializing fails.

        """
        try:
            super().__init__(group_dict_or_json)
        except JSONDecodeError as jdce:
            raise OPInvalidGroupException(
                f"Failed to unserialize group json: {jdce}", group_dict_or_json) from jdce

    @property
    def description(self) -> str:
        """
        The desc attribute
        """
        return self["description"]

    @property
    def state(self) -> str:
        return self["state"]

    @property
    def permissions(self) -> List[str]:
        return self["permissions"]

    @property
    def type(self) -> str:
        """
        str : The type attribute
        """
        return self["type"]


class OPUserDescriptor(OPAbstractObject):
    """
    A dictionary describing a user as returned by 'op list users'. This is a subset of a full OPUserOboject.
    """

    def __init__(self, user_descriptor_dict: Dict):
        super().__init__(user_descriptor_dict)

    @property
    def email(self) -> str:
        """
        str : The email attribute
        """
        return self["email"]

    @property
    def type(self) -> str:
        """
        str : The type attribute
        """
        return self["type"]

    @property
    def state(self) -> str:
        """
        str : The state attribute
        """
        return self["state"]


class OPUserDescriptorList(_OPDescriptorList[OPUserDescriptor]):
    """
    List of OPUserDescriptor dictionaries as returned from an 'op list users' operation
    These are not full user dictionaries as would be returned from 'op get user'.
    Rather, just a minimum set of fields to describe a user.

    Each user descriptor object has the following properties
    """

    def __init__(self, user_list_json):
        super().__init__()
        user_list = []
        try:
            user_list = json.loads(user_list_json)
        except JSONDecodeError as jdce:
            raise OPInvalidUserListException(
                f"Failed to unserialize user json: {jdce}", user_list_json)
        for user_obj in user_list:
            user_descriptor = OPUserDescriptor(user_obj)
            self.append(user_descriptor)


class OPGroupDescriptor(OPAbstractObject):
    """
    A dictionary describing a group as returned by 'op list groups'. This is a subset of a full OPGroupOboject.
    """

    # Override __init__ since parent class is abstract
    def __init__(self, dict_or_json: Union[str, dict]):
        super().__init__(dict_or_json)

    @property
    def description(self) -> str:
        """
        The desc attribute
        """
        return self["description"]

    @property
    def state(self) -> str:
        return self["state"]

    @property
    def created_at(self) -> datetime:
        """
        datetime : The created_at attribute parsed as a datetime object
        """
        created = self["created_at"]
        created = fromisoformat_z(created)
        return created


class OPGroupDescriptorList(_OPDescriptorList[OPGroupDescriptor]):
    """
    List of OPGroupDescriptor dictionaries as returned from an 'op list group' operation.
    These are not full group dictionaries as would be returned from 'op get group'.
    Rather, just a minimum set of fields to describe a group.

    Each group descriptor is a dictionary of str:str pairs, but in addition has the following
    convenience properties
    """

    def __init__(self, group_list_json):
        super().__init__()
        group_list = []
        try:
            group_list = json.loads(group_list_json)
        except JSONDecodeError as jdce:
            raise OPInvalidGroupListException(
                f"Failed to unserialize user json: {jdce}", group_list_json) from jdce
        for group_obj in group_list:
            group_descriptor = OPGroupDescriptor(group_obj)
            self.append(group_descriptor)


class OPVaultDescriptor(OPAbstractObject):
    """
    A dictionary describing a vault as returned by 'op list vaults'. This is a subset of
    a full vault object.
    """

    def __init__(self, vault_dict_or_json):
        super().__init__(vault_dict_or_json)


class OPVault(OPVaultDescriptor):
    """
    A dictionary of full details about a vault as returned by
    an 'op get vault' operation
    """

    def __init__(self, vault_dict_or_json):
        try:
            super().__init__(vault_dict_or_json)
        except JSONDecodeError as jdce:
            raise OPInvalidVaultException(
                f"Failed to unserialize vault json: {jdce}", vault_dict_or_json) from jdce

    @property
    def description(self) -> str:
        """
        str : The vault description
        """
        return self["description"]

    @property
    def item_count(self) -> int:
        return self["items"]

    @property
    def type(self) -> str:
        """
        str: The "type" attribute of the vault.
        """
        return self["type"]

    @property
    def created_at(self) -> datetime:
        """
        datetime : The created_at attribute parsed as a datetime object
        """
        created = self["created_at"]
        created = fromisoformat_z(created)
        return created

    @property
    def updated_at(self) -> datetime:
        """
        datetime : The updated_at attribute parsed as a datetime object
        """
        updated = self["updated_at"]
        updated = fromisoformat_z(updated)
        return updated


class OPVaultDescriptorList(_OPDescriptorList[OPVaultDescriptor]):
    """
    A list of OPVaultDescriptor dictionaries as returned by 'op list vaults'
    """

    def __init__(self, vault_list_json: str):
        super().__init__()
        vault_list = []
        try:
            vault_list = json.loads(vault_list_json)
        except JSONDecodeError as jdce:
            raise OPInvalidVaultListException(
                f"Failed to unserialize vault list JSON: {jdce}", vault_list_json) from jdce

        for vault_obj in vault_list:
            vault_descriptor = OPVaultDescriptor(vault_obj)
            self.append(vault_descriptor)
