import shlex
from typing import List, Optional, Union

from ._svc_account import OPSvcAcctSupportCode, OPSvcAcctSupportRegistry
from .op_items._new_item import OPNewItemMixin
from .op_items.password_recipe import OPPasswordRecipe


class _OPArgv(list):
    """
    This is essentially an 'argv' list with some additional methods, such as class methods
    for generating proper argument lists for specific 1Password operations.

    The primary purpose of this class is to facilitate the 'mock-op' project's automated response generation,
    as it allows the preciese set of command line arguments to be captured for later playback.
    """

    def __init__(self,
                 op_exe: str,
                 command: str,
                 args: List[str],
                 subcommands: Optional[Union[str, List[str]]] = None,
                 global_args: List[str] = [],
                 encoding="utf-8"):
        # TODO: Refactor this
        # constructor is getting too many specialized kwargs tied to
        # specific commands/subcommands
        # maybe instead of an "args" array plus a bunch of named kwargs,
        # send in a dict that gets passed through tree of argv building logic?

        argv = [op_exe]
        if not global_args:
            global_args = []
        else:
            global_args = list(global_args)

        if encoding.lower() != "utf-8":  # pragma: no coverage
            global_args.extend(["--encoding", encoding])

        for arg in global_args:
            argv.append(arg)
        if command:
            argv.append(command)
        self.command = command
        self.subcommands = None

        # whatever flags the command or subcommand take, plust global flags
        self.args_to_command = args

        if subcommands:
            if isinstance(subcommands, str):
                subcommands = [subcommands]
            else:
                subcommands = list(subcommands)  # pragma: no cover
            self.subcommands = subcommands
            argv.extend(subcommands)
        argv.extend(args)
        super().__init__(argv)

    def cmd_str(self):
        """
        return a shell-escaped command string from this argv
        """
        cmd_str = shlex.join(self)
        return cmd_str

    def svc_account_supported(self) -> OPSvcAcctSupportCode:
        # OPSvcAcctSupportRegistry is a singleton
        # so this is fine
        reg = OPSvcAcctSupportRegistry()
        supported = reg.command_supported(self)
        return supported

    @classmethod
    def item_generic_argv(cls,
                          op_exe: str,
                          subcommands: Optional[Union[str, List[str]]],
                          sub_cmd_args: Optional[List[str]] = None):
        args = []
        global_args = ["--format", "json"]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe,
                   "item",
                   args,
                   subcommands=subcommands,
                   global_args=global_args)
        return argv

    @classmethod
    def item_get_argv(cls,
                      op_exe,
                      item_name_or_id,
                      vault=None,
                      fields=None,
                      include_archive=False):
        sub_cmd_args = [item_name_or_id]
        if vault:
            sub_cmd_args.extend(["--vault", vault])

        if fields:
            sub_cmd_args.extend(["--fields", fields])
        if include_archive:
            sub_cmd_args.append("--include-archive")
        argv = cls.item_generic_argv(op_exe, "get", sub_cmd_args)
        return argv

    @classmethod
    def item_get_totp_argv(cls, op_exe, item_name_or_id, vault=None):
        field_arg = "type=otp"

        argv = cls.item_get_argv(
            op_exe, item_name_or_id, vault=vault, fields=field_arg)
        return argv

    @classmethod
    def document_generic_argv(cls,
                              op_exe: str,
                              subcommands: Optional[Union[str, List[str]]],
                              sub_cmd_args: Optional[List[str]]):
        args = []
        global_args = ["--format", "json"]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe,
                   "document",
                   args,
                   subcommands=subcommands,
                   global_args=global_args)
        return argv

    @classmethod
    def document_get_argv(cls, op_exe, document_name_or_id, vault=None, include_archive=False):

        sub_cmd_args = [document_name_or_id]
        if vault:
            sub_cmd_args.extend(["--vault", vault])
        if include_archive:
            sub_cmd_args.append("--include-archive")
        argv = cls.document_generic_argv(op_exe, "get", sub_cmd_args)
        return argv

    @classmethod
    def vault_generic_argv(cls,
                           op_exe: str,
                           subcommands: Optional[Union[str, List[str]]],
                           sub_cmd_args: Optional[List[str]]):
        args = []
        global_args = ["--format", "json"]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe, "vault", args, subcommands=subcommands,
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
    def user_generic_argv(cls,
                          op_exe: str,
                          subcommands: Optional[Union[str, List[str]]],
                          sub_cmd_args: Optional[List[str]]):
        args = []
        global_args = ["--format", "json"]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe, "user", args, subcommands=subcommands,
                   global_args=global_args)
        return argv

    @classmethod
    def user_get_argv(cls, op_exe, user_name_or_id):
        sub_cmd_args = [user_name_or_id]
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
    def group_generic_argv(cls,
                           op_exe: str,
                           subcommands: Optional[Union[str, List[str]]],
                           sub_cmd_args: Optional[List[str]]):
        args = []
        global_args = ["--format", "json"]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe, "group", args, subcommands=subcommands,
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
    def item_template_list_argv(cls, op_exe):  # pragma: no cover
        # subcommands may be a string or list
        # so no need to put the sub-subcommand
        # into an arg list
        sub_commands = ["template", "list"]
        sub_cmd_args: List[str] = []

        argv_obj = cls.item_generic_argv(op_exe, sub_commands, sub_cmd_args)
        return argv_obj

    @classmethod
    def whoami_argv(cls, op_exe, account=None):
        args: List[str] = []
        global_args = []
        if account:
            global_args = ["--account", account]
        global_args.extend(["--format", "json"])
        argv_obj = cls(op_exe, "whoami", args, global_args=global_args)
        return argv_obj

    @classmethod
    def cli_version_argv(cls, op_exe):
        args: List[str] = []
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
    def account_generic_argv(cls,
                             op_exe: str,
                             subcommands: Optional[Union[str, List[str]]],
                             sub_cmd_args: Optional[List[str]] = None,
                             encoding: str = "utf-8"):
        args = []
        cmd = "account"
        global_args = ["--format", "json"]
        if sub_cmd_args:  # pragma: no coverage
            args.extend(sub_cmd_args)
        argv = cls(op_exe, cmd, args, subcommands=subcommands,
                   global_args=global_args, encoding=encoding)
        return argv

    @classmethod
    def account_list_argv(cls, op_exe, encoding="utf-8"):
        subcmd = "list"
        argv = cls.account_generic_argv(
            op_exe, subcmd, encoding=encoding)
        return argv

    @classmethod
    def account_forget_argv(cls, op_exe, account):  # pragma: no coverage
        subcmd = "forget"
        sub_cmd_args = [account]
        argv = cls.account_generic_argv(
            op_exe, subcmd, sub_cmd_args=sub_cmd_args)

        return argv

    @classmethod
    def item_create_argv(cls,
                         op_exe,
                         item: OPNewItemMixin,
                         password_recipe: Optional[OPPasswordRecipe] = None,
                         vault: Optional[str] = None,
                         encoding="utf-8"):
        """
        op item create --template ./new_item.json --vault "Test Data" --generate-password=20,letters,digits --dry-run --format json
        """
        template_filename = item.secure_tempfile(
            encoding=encoding)

        item_create_args = ["--template", template_filename]

        if password_recipe:
            # '--password-recipe' requires an '=' unlike other option/argument pairs
            item_create_args.append(f"--generate-password={password_recipe}")
        if vault:
            item_create_args.extend(["--vault", vault])
        argv = cls.item_generic_argv(op_exe, "create")
        return argv

    @classmethod
    def item_delete_argv(cls,
                         op_exe: str,
                         item_name_or_id: str,
                         vault: Optional[str] = None,
                         archive: bool = False):
        sub_cmd_args = [item_name_or_id]
        if archive:
            sub_cmd_args.append("--archive")
        if vault:
            sub_cmd_args.extend(["--vault", vault])
        delete_argv = cls.item_generic_argv(op_exe, "delete", sub_cmd_args)

        return delete_argv

    @classmethod
    def document_delete_argv(cls,
                             op_exe: str,
                             document_name_or_id: str,
                             vault: Optional[str] = None,
                             archive: bool = False):
        sub_cmd_args = [document_name_or_id]
        if archive:
            sub_cmd_args.append("--archive")
        if vault:
            sub_cmd_args.extend(["--vault", vault])
        delete_argv = cls.document_generic_argv(op_exe, "delete", sub_cmd_args)

        return delete_argv
