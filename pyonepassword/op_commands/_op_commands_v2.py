import logging

from .._argv_generator import OPArgvGenerator
from ..op_cli_version import MINIMUM_VERSION_2, MINIMUM_VERSION_3
from ._op_commands_abstract import (
    _OPCommandInterfaceAbstract,
    _OPCommandRegistry
)

from ..py_op_exceptions import (
    OPCmdFailedException,
    OPGetItemException
)


class _OPCommandV2(_OPCommandInterfaceAbstract, metaclass=_OPCommandRegistry):
    MIN_CLI_VERSION = MINIMUM_VERSION_2
    MAX_CLI_VERSION = MINIMUM_VERSION_3
    """
    A class that directly maps methods to `op` commands
    & subcommands.
    No convenience methods are provided.
    No responses are parsed.
    """

    def __init__(self, op_exe, vault=None, logger=None):
        self._op_exe = op_exe
        self.vault = vault
        if not logger:
            logging.basicConfig(format="%(message)s", level=logging.DEBUG)
            logger = logging.getLogger()
        self.logger = logger
        self._argv_generator = OPArgvGenerator(self.cli_version)

    def _item_get_argv(self, item_name_or_uuid, vault=None, field_labels=[]):
        vault_arg = vault if vault else self.vault

        lookup_argv = self._argv_generator.item_get_argv(
            self._op_exe, item_name_or_uuid, vault=vault_arg, field_labels=field_labels)
        return lookup_argv

    def _get_item(self, item_name_or_uuid, vault=None, fields=None, decode="utf-8"):
        item_get_argv = self._item_get_argv(
            item_name_or_uuid, vault=vault, field_labels=fields)
        try:
            output = self._op_exe._run(
                item_get_argv, capture_stdout=True, decode=decode)
        except OPCmdFailedException as ocfe:
            raise OPGetItemException.from_opexception(ocfe) from ocfe

        return output
