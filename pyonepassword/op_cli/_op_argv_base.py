import shlex

from typing import List


class _OPArgvBase(list):
    """
    This is essentially an 'argv' list with some additional methods, such as class methods
    for generating proper argument lists for specific 1Password operations.

    The primary purpose of this class is to facilitate the 'mock-op' project's automated response generation,
    as it allows the preciese set of command line arguments to be captured for later playback.
    """

    def __init__(self, op_exe: str, command: str, args: List, subcommand: str = None, global_args=[]):
        # TODO: Refactor this
        # constructor is getting too many specialized kwargs tied to
        # specific commands/subcommands
        # maybe instead of an "args" array plus a bunch of named kwargs,
        # send in a dict that gets passed through tree of argv building logic?
        argv = [str(op_exe)]
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

    def query_args(self):
        args = list(self[1:])
        return args

    def cmd_str(self):
        """
        return a shell-escaped command string from this argv
        """
        cmd_str = shlex.join(self)
        return cmd_str

    @classmethod
    def normal_signin_argv(cls, op_exe, account_shorthand=None):
        global_args = []
        if account_shorthand:
            global_args = ["--account", account_shorthand]
        argv = [account_shorthand, "--raw"]
        return cls(op_exe, "signin", argv, global_args=global_args)

    @classmethod
    def cli_version_argv(cls, op_exe):
        args = []
        global_args = ["--version"]
        argv_obj = cls(op_exe, None, args, global_args=global_args)
        return argv_obj

    @classmethod
    def signout_argv(cls, op_exe, account_shorthand: str, session: str, forget=False):
        global_args = ["--account", account_shorthand, "--session", session]
        signout_args = []
        if forget:
            signout_args.append("--forget")
        argv = cls(op_exe, "signout", signout_args, global_args=global_args)
        return argv

    @classmethod
    def _create_item_argv(cls, op_exe, template_filename, item_name, url=None, category=None, vault: str = None, encoding="utf=8"):
        raise NotImplementedError()
