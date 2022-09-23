import shlex
from typing import List


class _OPArgv(list):
    """
    This is essentially an 'argv' list with some additional methods, such as class methods
    for generating proper argument lists for specific 1Password operations.

    The primary purpose of this class is to facilitate the 'mock-op' project's automated response generation,
    as it allows the preciese set of command line arguments to be captured for later playback.
    """

    def __init__(self, op_exe: str, command: str, args: List, subcommand: str = None, cache=False, global_args=[], encoding="utf-8"):
        # TODO: Refactor this
        # constructor is getting too many specialized kwargs tied to
        # specific commands/subcommands
        # maybe instead of an "args" array plus a bunch of named kwargs,
        # send in a dict that gets passed through tree of argv building logic?
        argv = [op_exe]
        if encoding.lower() != "utf-8":
            global_args.extend(["--encoding", encoding])
        if cache:
            global_args.append("--cache")
        for arg in global_args:
            argv.append(arg)
        if command:
            argv.append(command)
        self.command = command
        self.subcommand = None

        # whatever flags the command or subcommand take, plust global flags
        self.args_to_command = args

        if subcommand:
            self.subcommand = subcommand
            argv.extend([subcommand])
        argv.extend(args)
        super().__init__(argv)

    def cmd_str(self):
        """
        return a shell-escaped command string from this argv
        """
        cmd_str = shlex.join(self)
        return cmd_str

    @classmethod
    def item_generic_argv(cls, op_exe, item_subcommand, sub_cmd_args):
        args = []
        global_args = ["--format", "json"]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe, "item", args, subcommand=item_subcommand,
                   global_args=global_args)
        return argv

    @classmethod
    def item_get_argv(cls, op_exe, item_name_or_id, vault=None, fields=None):
        sub_cmd_args = [item_name_or_id]
        if vault:
            sub_cmd_args.extend(["--vault", vault])

        if fields:
            sub_cmd_args.extend(["--fields", fields])
        argv = cls.item_generic_argv(op_exe, "get", sub_cmd_args)
        return argv

    @classmethod
    def item_get_totp_argv(cls, op_exe, item_name_or_id, vault=None):
        sub_cmd_args = []
        field_arg = "type=otp"
        if vault:
            sub_cmd_args.extend(["--vault", vault])

        argv = cls.item_get_argv(
            op_exe, item_name_or_id, vault=vault, fields=field_arg)
        return argv

    @classmethod
    def document_generic_argv(cls, op_exe, doc_subcommand, sub_cmd_args):
        args = []
        global_args = ["--format", "json"]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe, "document", args,
                   subcommand=doc_subcommand, global_args=global_args)
        return argv

    @classmethod
    def document_get_argv(cls, op_exe, document_name_or_id, vault=None):
        sub_cmd_args = [document_name_or_id]
        if vault:
            sub_cmd_args.extend(["--vault", vault])
        argv = cls.document_generic_argv(op_exe, "get", sub_cmd_args)
        return argv

    @classmethod
    def vault_generic_argv(cls, op_exe, vault_subcommand, sub_cmd_args):
        args = []
        global_args = ["--format", "json"]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe, "vault", args, subcommand=vault_subcommand,
                   global_args=global_args)
        return argv

    @classmethod
    def vault_get_argv(cls, op_exe, vault_name_or_id):
        sub_cmd_args = [vault_name_or_id]
        argv = cls.vault_generic_argv(op_exe, "get", sub_cmd_args)
        return argv

    @classmethod
    def vault_list_argv(cls, op_exe, group_name_or_id=None, user_name_or_id=None):
        sub_cmd_args = []
        if group_name_or_id:
            sub_cmd_args.extend(["--group", group_name_or_id])
        if user_name_or_id:
            sub_cmd_args.extend(["--user", user_name_or_id])
        argv = cls.vault_generic_argv(op_exe, "list", sub_cmd_args)
        return argv

    @classmethod
    def user_generic_argv(cls, op_exe, vault_subcommand, sub_cmd_args):
        args = []
        global_args = ["--format", "json"]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe, "user", args, subcommand=vault_subcommand,
                   global_args=global_args)
        return argv

    @classmethod
    def user_get_argv(cls, op_exe, user_name_or_id):
        sub_cmd_args = [user_name_or_id]
        argv = cls.user_generic_argv(op_exe, "get", sub_cmd_args)
        return argv

    @classmethod
    def user_get_signed_in_argv(cls, op_exe):
        sub_cmd_args = ["--me"]
        argv = cls.user_generic_argv(op_exe, "get", sub_cmd_args)
        return argv

    @classmethod
    def user_list_argv(cls, op_exe, group_name_or_id=None, vault=None):
        sub_cmd_args = []
        if group_name_or_id:
            sub_cmd_args.extend(["--group", group_name_or_id])
        if vault:
            sub_cmd_args.extend(["--vault", vault])
        argv = cls.user_generic_argv(op_exe, "list", sub_cmd_args)
        return argv

    @classmethod
    def group_generic_argv(cls, op_exe, vault_subcommand, sub_cmd_args):
        args = []
        global_args = ["--format", "json"]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe, "group", args, subcommand=vault_subcommand,
                   global_args=global_args)
        return argv

    @classmethod
    def group_get_argv(cls, op_exe, user_name_or_id):
        sub_cmd_args = [user_name_or_id]
        argv = cls.group_generic_argv(op_exe, "get", sub_cmd_args)
        return argv

    @classmethod
    def group_list_argv(cls, op_exe, user_name_or_id=None, vault=None):
        sub_cmd_args = []
        if user_name_or_id:
            sub_cmd_args.extend(["--user", user_name_or_id])
        if vault:
            sub_cmd_args.extend(["--vault", vault])
        argv = cls.group_generic_argv(op_exe, "list", sub_cmd_args)
        return argv

    @classmethod
    def normal_signin_argv(cls, op_exe, account=None):
        global_args = []
        if account:
            global_args = ["--account", account]
        argv = ["--raw"]
        return cls(op_exe, "signin", argv, global_args=global_args)

    @classmethod
    def item_template_list_argv(cls, op_exe):
        sub_command = "template"
        sub_cmd_args = ["list"]

        argv_obj = cls.item_generic_argv(op_exe, sub_command, sub_cmd_args)
        return argv_obj

    @classmethod
    def whoami_argv(cls, op_exe, account=None):
        args = []
        global_args = []
        if account:
            global_args = ["--account", account]
        global_args.extend(["--format", "json"])
        argv_obj = cls(op_exe, "whoami", args, global_args=global_args)
        return argv_obj

    @classmethod
    def cli_version_argv(cls, op_exe):
        args = []
        global_args = ["--version"]
        argv_obj = cls(op_exe, None, args, global_args=global_args)
        return argv_obj

    @classmethod
    def signout_argv(cls, op_exe, account_shorthand: str, session: str, forget=False, uses_bio=False):  # pragma: no cover
        global_args = []
        if not uses_bio:
            global_args = ["--account",
                           account_shorthand, "--session", session]
        signout_args = []
        if forget:
            signout_args.append("--forget")
        argv = cls(op_exe, "signout", signout_args, global_args=global_args)
        return argv

    @classmethod
    def forget_argv(cls, op_exe, account_shorthand):  # pragma: no cover
        forget_args = [account_shorthand]
        argv = cls(op_exe, "forget", forget_args)
        return argv

    @classmethod
    def item_list_argv(cls, op_exe, categories=[], include_archive=False, tags=[], vault=None):
        item_list_args = []
        if categories:
            categories_arg = ",".join(categories)
            item_list_args.extend(["--categories", categories_arg])
        if include_archive:
            item_list_args.append("--include-archive")
        if tags:
            tags_args = ",".join(tags)
            item_list_args.extend(["--tags", tags_args])
        if vault:
            item_list_args.extend(["--vault", vault])

        argv = cls.item_generic_argv(op_exe, "list", item_list_args)
        return argv

    @classmethod
    def account_list_argv(cls, op_exe, output_format="json", encoding="utf-8"):
        cmd = "account"
        cmd_args = []
        subcmd = "list"
        global_args = ["--format", output_format]
        argv = cls(op_exe, cmd, cmd_args, subcommand=subcmd,
                   global_args=global_args, encoding=encoding)
        return argv
