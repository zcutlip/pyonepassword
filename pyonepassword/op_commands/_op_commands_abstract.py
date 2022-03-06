from abc import abstractclassmethod, abstractmethod

from ..op_cli import OPArgvCommon
from ..op_cli_version import OPCLIVersion
from ..op_items._op_items_base import OPAbstractItem


class _OPCommandRegistryException(Exception):
    pass


class _OPCommandRegistry(type):

    _registry = {}

    def __new__(cls, clsname, bases, dct, *args, **kwargs):
        newclass = super().__new__(cls, clsname, bases, dct)
        if newclass.MIN_CLI_VERSION and newclass.MAX_CLI_VERSION:
            version_tuple = (newclass.MIN_CLI_VERSION,
                             newclass.MAX_CLI_VERSION)
            if version_tuple in cls._registry:
                raise _OPCommandRegistryException(
                    f"Version tuple already registered: {version_tuple}")
            cls._registry[version_tuple] = newclass
        return newclass

    @classmethod
    def op_command_class(cls, op_version: OPCLIVersion):
        op_class = None
        for vtuple, cmd_class in cls._registry.items():
            low, hi = vtuple
            if low <= op_version and op_version < hi:
                op_class = cmd_class
                break
        if op_class is None:
            raise _OPCommandRegistryException(
                f"No _OPCommandInterface class for version {op_version}")
        return op_class


class _OPCommandInterfaceAbstract:

    @abstractmethod
    def __init__(self, op_path_or_exe, vault=None, logger=None, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def supports_item_creation(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def _get_item_argv(self, item_name_or_uuid, vault=None, fields=None) -> OPArgvCommon:
        raise NotImplementedError()

    @abstractmethod
    def _get_totp_argv(self, item_name_or_uuid, vault=None):
        raise NotImplementedError()

    @abstractmethod
    def _get_document_argv(self, document_name_or_uuid: str, vault: str = None):
        raise NotImplementedError()

    @abstractmethod
    def _get_user_argv(self, user_name_or_uuid: str):
        raise NotImplementedError()

    @abstractmethod
    def _get_group_argv(self, group_name_or_uuid: str):
        raise NotImplementedError()

    @abstractmethod
    def _get_vault_argv(self, vault_name_or_uuid: str):
        raise NotImplementedError()

    @abstractmethod
    def _get_item(self, item_name_or_uuid, vault=None, fields=None, decode="utf-8"):
        raise NotImplementedError()

    @abstractmethod
    def _get_totp(self, item_name_or_uuid, vault=None, decode="utf-8"):
        raise NotImplementedError()

    @abstractmethod
    def _get_document(self, document_name_or_uuid: str, vault: str = None):
        raise NotImplementedError()

    @abstractmethod
    def _get_user(self, user_name_or_uuid: str, decode: str = "utf-8") -> str:
        raise NotImplementedError()

    @abstractmethod
    def _get_group(self, group_name_or_uuid: str, decode: str = "utf-8") -> str:
        raise NotImplementedError()

    @abstractmethod
    def _get_vault(self, vault_name_or_uuid: str, decode: str = "utf-8") -> str:
        raise NotImplementedError()

    @abstractmethod
    def _create_item(self, item: OPAbstractItem, item_name, vault=None):
        raise NotImplementedError()

    @abstractmethod
    def _signout(self, account, session, forget=False):
        raise NotImplementedError()

    @abstractclassmethod
    def _forget(cls, account: str, op_path='op'):
        raise NotImplementedError()

    @abstractmethod
    def _create_item_argv(self, item, item_name, vault):
        raise NotImplementedError()

    @abstractmethod
    def _list_items_argv(self, categories=[], include_archive=False, tags=[], vault=None):
        raise NotImplementedError()

    @abstractmethod
    def _list_items(self, categories=[], include_archive=False, tags=[], vault=None, decode="utf-8"):
        raise NotImplementedError()

    @property
    def cli_version(self) -> OPCLIVersion:
        return self._op_exe.cli_version
