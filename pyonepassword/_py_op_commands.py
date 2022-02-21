"""
Description: A module that maps methods to to `op` commands and subcommands
"""

from .op_cli._py_op_cli import _OPCLIExecute
from ._argv_generator import OPArgvGenerator

from .py_op_exceptions import (
    OPCmdFailedException,
    OPCreateItemException,
    OPCreateItemNotSupportedException,
    OPGetGroupException,
    OPGetItemException,
    OPGetDocumentException,
    OPGetUserException,
    OPGetVaultException
)

from .op_cli_version import MINIMUM_ITEM_CREATION_VERSION
from .op_items._op_items_base import OPAbstractItem


class _OPCommandInterface(_OPCLIExecute):
    """
    A class that directly maps methods to `op` commands
    & subcommands.
    No convenience methods are provided.
    No responses are parsed.
    """

    def __init__(self, vault=None, **kwargs):
        super().__init__(**kwargs)
        self.vault = vault
        self._argv_generator = OPArgvGenerator(self.op_path)

    def supports_item_creation(self):
        support = False
        if self._cli_version >= MINIMUM_ITEM_CREATION_VERSION:
            support = True
        return support

    def _get_item_argv(self, item_name_or_uuid, vault=None, fields=None):
        vault_arg = vault if vault else self.vault

        lookup_argv = self._argv_generator.get_item_argv(
            self.op_path, item_name_or_uuid, vault=vault_arg, fields=fields)
        return lookup_argv

    def _get_totp_argv(self, item_name_or_uuid, vault=None):
        vault_arg = vault if vault else self.vault

        lookup_argv = self._argv_generator.get_totp_argv(
            self.op_path, item_name_or_uuid, vault=vault_arg)
        return lookup_argv

    def _get_document_argv(self, document_name_or_uuid: str, vault: str = None):
        vault_arg = vault if vault else self.vault

        get_document_argv = self._argv_generator.get_document_argv(
            self.op_path, document_name_or_uuid, vault=vault_arg)

        return get_document_argv

    def _get_user_argv(self, user_name_or_uuid: str):
        get_user_argv = self._argv_generator.get_generic_argv(
            self.op_path, "user", user_name_or_uuid, [])
        return get_user_argv

    def _get_group_argv(self, group_name_or_uuid: str):
        get_group_argv = self._argv_generator.get_generic_argv(
            self.op_path, "group", group_name_or_uuid, [])
        return get_group_argv

    def _get_vault_argv(self, vault_name_or_uuid: str):
        get_vault_argv = self._argv_generator.get_generic_argv(
            self.op_path, "vault", vault_name_or_uuid, [])
        return get_vault_argv

    def _cli_version_argv(self):
        # Specifically for use by mock_op response-generator
        cli_version_argv = self._argv_generator.cli_version_argv(self.op_path)
        return cli_version_argv

    def _get_item(self, item_name_or_uuid, vault=None, fields=None, decode="utf-8"):
        get_item_argv = self._get_item_argv(
            item_name_or_uuid, vault=vault, fields=fields)
        try:
            output = self._run(
                get_item_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPGetItemException.from_opexception(ocfe) from ocfe

        return output

    def _get_totp(self, item_name_or_uuid, vault=None, decode="utf-8"):
        get_totp_argv = self._get_totp_argv(
            item_name_or_uuid, vault=vault)
        try:
            output = self._run(
                get_totp_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPGetItemException.from_opexception(ocfe) from ocfe

        return output

    def _get_document(self, document_name_or_uuid: str, vault: str = None):
        """
        Download a document object from a 1Password vault by name or UUID.

        Arguments:
            - 'item_name_or_uuid': The item to look up
        Raises:
            - OPGetDocumentException if the lookup fails for any reason.
            - OPNotFoundException if the 1Password command can't be found.
        Returns:
            - Bytes: document bytes
        """

        get_document_argv = self._get_document_argv(
            document_name_or_uuid, vault=vault)

        try:
            document_bytes = self._run(get_document_argv, capture_stdout=True)
        except OPCmdFailedException as ocfe:
            raise OPGetDocumentException.from_opexception(ocfe) from ocfe

        return document_bytes

    def _get_user(self, user_name_or_uuid: str, decode: str = "utf-8") -> str:
        get_user_argv = self._get_user_argv(user_name_or_uuid)
        try:
            output = self._run(
                get_user_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPGetUserException.from_opexception(ocfe) from ocfe
        return output

    def _get_group(self, group_name_or_uuid: str, decode: str = "utf-8") -> str:
        get_group_argv = self._get_group_argv(group_name_or_uuid)
        try:
            output = self._run(
                get_group_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPGetGroupException.from_opexception(ocfe) from ocfe
        return output

    def _get_vault(self, vault_name_or_uuid: str, decode: str = "utf-8") -> str:
        get_vault_argv = self._get_vault_argv(vault_name_or_uuid)
        try:
            output = self._run(
                get_vault_argv, capture_stdout=True, decode=decode
            )
        except OPCmdFailedException as ocfe:
            raise OPGetVaultException.from_opexception(ocfe)
        return output

    def _create_item(self, item: OPAbstractItem, item_name, vault=None):
        if not self.supports_item_creation():
            msg = f"Minimum supported 'op' version for item creation: {MINIMUM_ITEM_CREATION_VERSION}, current version: {self._cli_version}"
            raise OPCreateItemNotSupportedException(msg)
        argv = self._create_item_argv(item, item_name, vault)
        try:
            output = self._run(
                argv, capture_stdout=True, decode="utf-8"
            )
        except OPCmdFailedException as ocfe:
            raise OPCreateItemException.from_opexception(ocfe)

        return output

    def _signout(self, account, session, forget=False):
        argv = self._argv_generator.signout_argv(
            self.op_path, account, session, forget=forget)
        self._run(argv)

    @classmethod
    def _forget(cls, account: str, op_path='op'):
        generator = OPArgvGenerator(op_path)
        if not op_path:
            op_path = cls.OP_PATH
        argv = generator.forget_argv(op_path, account)
        cls._run(argv)

    def _create_item_argv(self, item, item_name, vault):
        vault_arg = vault if vault else self.vault
        create_item_argv = self._argv_generator.create_item_argv(
            self.op_path, item, item_name, vault=vault_arg
        )
        return create_item_argv

    def _list_items_argv(self, categories=[], include_archive=False, tags=[], vault=None):
        vault_arg = vault if vault else self.vault
        list_items_argv = self._argv_generator.list_items_argv(
            self.op_path, categories=categories, include_archive=include_archive, tags=tags, vault=vault_arg)
        return list_items_argv

    def _list_items(self, categories=[], include_archive=False, tags=[], vault=None, decode="utf-8"):
        argv = self._list_items_argv(
            categories=categories, include_archive=include_archive, tags=tags, vault=vault)
        try:
            output = self._run(argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as e:
            raise e
        return output
