from typing import List

from ._op_argv_base import _OPArgvBase


class _OPArgv(_OPArgvBase):

    def __init__(self, op_exe: str, command: str, subcommand: str = None,  args: List = [], global_args=[]):
        args.extend(["--format", "json"])
        super().__init__(op_exe, command, args, subcommand, global_args)

    @classmethod
    def get_verify_signin_argv(cls, op_exe):
        sub_cmd = "template"
        sub_cmd_args = ["list"]
        argv_obj = cls.item_generic_argv(
            op_exe, sub_cmd, sub_cmd_args=sub_cmd_args)
        return argv_obj

    @classmethod
    def item_generic_argv(cls, op_exe, item_subcommand, sub_cmd_args=[], global_args=[]):
        command = "item"
        args = []
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv_obj = cls(op_exe, command, subcommand=item_subcommand, args=args)
        return argv_obj

    @classmethod
    def item_get_argv(cls, op_exe, item_name_or_uuid, vault=None, field_labels=[]):
        sub_cmd_args = [item_name_or_uuid]
        if vault:
            sub_cmd_args.extend(["--vault", vault])
        if field_labels:
            # ultimate arg needs to be
            # "--fields label=foo,label=bar"

            # first generate ["label=foo", "label-bar"]
            field_labels = [f"label={f}" for f in field_labels]
            # now generate "label=foo,label=bar"
            label_string = ",".join(field_labels)
            # and now "--fields label=foo,label=bar"
            sub_cmd_args.extend("--fields", label_string)
        argv_obj = cls.item_generic_argv(
            op_exe, "get", sub_cmd_args=sub_cmd_args)
        return argv_obj

    @classmethod
    def get_generic_argv(cls, op_exe, get_subcommand, obj_identifier, sub_cmd_args):
        args = [obj_identifier]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe, "get", args, subcommand=get_subcommand)
        return argv

    @classmethod
    def get_item_argv(cls, op_exe, item_name_or_uuid, vault=None, fields=None):
        sub_cmd_args = []
        if vault:
            sub_cmd_args.extend(["--vault", vault])

        if fields:
            sub_cmd_args.extend(["--fields", fields])
        argv = cls.get_generic_argv(
            op_exe, "item", item_name_or_uuid, sub_cmd_args)
        return argv
