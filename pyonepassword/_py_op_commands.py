"""
Description: A module that maps methods to to `op` commands and subcommands
"""

from ._py_op_cli import (
    _OPCLIExecute,
    _OPArgv
)
from .py_op_exceptions import (
    OPCmdFailedException,
    OPGetItemException,
    OPGetDocumentException
)


class _OPCommandInterface(_OPCLIExecute):
    """
    A class that directly maps methods to `op` commands
    & subcommands.
    No convenience methods are provide.
    No responses are parsed.
    """

    def __init__(self, vault=None, account_shorthand=None, signin_address=None, email_address=None,
                 secret_key=None, password=None, logger=None, op_path='op'):
        super().__init__(account_shorthand=account_shorthand,
                         signin_address=signin_address,
                         email_address=email_address,
                         secret_key=secret_key,
                         password=password,
                         logger=logger,
                         op_path=op_path)
        self.vault = vault

    def _get_item_argv(self, item_name_or_uuid, vault=None, fields=None):
        vault_arg = vault if vault else self.vault

        lookup_argv = _OPArgv.get_item_argv(
            self.op_path, item_name_or_uuid, vault=vault_arg, fields=fields)
        return lookup_argv

    def _get_document_argv(self, document_name_or_uuid: str, vault: str = None):
        vault_arg = vault if vault else self.vault

        get_document_argv = _OPArgv.get_document_argv(
            self.op_path, document_name_or_uuid, vault=vault_arg)

        return get_document_argv

    def get_item(self, item_name_or_uuid, vault=None, fields=None, decode="utf-8"):
        get_item_argv = self._get_item_argv(
            item_name_or_uuid, vault=vault, fields=fields)
        try:
            output = self._run(
                get_item_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPGetItemException.from_opexception(ocfe) from ocfe

        return output

    def get_document(self, document_name_or_uuid: str, vault: str = None):
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
