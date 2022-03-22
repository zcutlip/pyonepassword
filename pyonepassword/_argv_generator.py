from .op_cli_version import OPCLIVersion, MINIMUM_VERSION_2
from .op_cli import OPArgvCommon, OPArgvV1
from .op_cli import _OPCLIExecute


class OPArgvGenerator:

    def __init__(self, op_exe, decode="utf-8"):
        argv = self.cli_version_argv(op_exe)
        version_output = _OPCLIExecute._run(
            argv, capture_stdout=True, decode=decode)
        version = OPCLIVersion(version_output)
        self._op_argv = None
        if version < MINIMUM_VERSION_2:
            self._op_argv = OPArgvV1
        self.version = version

    def cli_version_argv(self, op_exe):
        argv = OPArgvCommon.cli_version_argv(op_exe)
        return argv

    def get_generic_argv(self, op_exe, get_subcommand, obj_identifier, sub_cmd_args):
        argv = self._op_argv.get_generic_argv(
            op_exe, get_subcommand, obj_identifier, sub_cmd_args)
        return argv

    def get_item_argv(self, op_exe, item_name_or_uuid, vault=None, fields=None):
        argv = self._op_argv.get_item_argv(
            op_exe, item_name_or_uuid, vault=vault, fields=fields)
        return argv

    def get_totp_argv(self, op_exe, item_name_or_uuid, vault=None):
        argv = self._op_argv.get_totp_argv(
            op_exe, item_name_or_uuid, vault=vault)
        return argv

    def get_document_argv(self, op_exe, document_name_or_uuid, vault=None):
        argv = self._op_argv.get_document_argv(
            op_exe, document_name_or_uuid, vault=vault)
        return argv
