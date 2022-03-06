from .op_cli import OPArgvCommon
from .op_cli._op_argv_v1 import _OPArgv as OPArgv_V1
from .op_cli_version import MINIMUM_VERSION_2


class OPArgvGenerator:

    def __init__(self, cli_version, decode="utf-8"):
        self._op_argv = None
        if cli_version < MINIMUM_VERSION_2:
            self._op_argv = OPArgv_V1
        self.version = cli_version

    def normal_signin_argv(self, op_exe, account_shorthand=None):
        argv = self._op_argv.normal_signin_argv(
            op_exe, account_shorthand=account_shorthand)
        return argv

    def get_verify_signin_argv(self, op_exe):
        argv = self._op_argv.get_verify_signin_argv(op_exe)
        return argv

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
