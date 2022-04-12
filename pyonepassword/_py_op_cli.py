import logging

import subprocess
import shlex
from os import environ as env
from typing import List

from .op_items._op_items_base import OPAbstractItem

from .py_op_exceptions import (
    OPNotFoundException,
    OPCmdFailedException,
    OPInvalidItemException
)


"""
Module to hold stuff that interacts directly with 'op' or its config

TODO: Move other code that closely touches 'op' here
"""


class _OPCLIExecute:
    NOT_SIGNED_IN_TEXT = "not currently signed in"

    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    logger = logging.getLogger()
    """
    Class for logging into and querying a 1Password account via the 'op' cli command.
    """

    @classmethod
    def _run_raw(cls, argv, input_string=None, capture_stdout=False, ignore_error=False):
        stdout = subprocess.PIPE if capture_stdout else None
        if input_string:
            if isinstance(input_string, str):
                input_string = input_string.encode("utf-8")

        _ran = subprocess.run(
            argv, input=input_string, stderr=subprocess.PIPE, stdout=stdout, env=env)

        stdout = _ran.stdout
        stderr = _ran.stderr
        returncode = _ran.returncode

        if not ignore_error:
            try:
                _ran.check_returncode()
            except subprocess.CalledProcessError as err:
                stderr_output = stderr.decode("utf-8").rstrip()
                raise OPCmdFailedException(stderr_output, returncode) from err

        return (stdout, stderr, returncode)

    @classmethod
    def _run(cls, argv, capture_stdout=False, input_string=None, decode=None):
        cls.logger.debug(f"Running: {argv.cmd_str()}")
        output = None
        try:
            output, _, _ = cls._run_raw(
                argv, input_string=input_string, capture_stdout=capture_stdout)
            if decode:
                output = output.decode(decode)
        except FileNotFoundError as err:
            cls.logger.error(
                "1Password 'op' command not found at: {}".format(argv[0]))
            cls.logger.error(
                "See https://support.1password.com/command-line-getting-started/ for more information,")
            cls.logger.error(
                "or install from Homebrew with: 'brew install 1password-cli")
            raise OPNotFoundException(argv[0], err.errno) from err

        return output


class _OPArgv(list):
    """
    This is essentially an 'argv' list with some additional methods, such as class methods
    for generating proper argument lists for specific 1Password operations.

    The primary purpose of this class is to facilitate the 'mock-op' project's automated response generation,
    as it allows the preciese set of command line arguments to be captured for later playback.
    """

    def __init__(self, op_exe: str, command: str, args: List, subcommand: str = None, global_args=[], encoding="utf-8"):
        # TODO: Refactor this
        # constructor is getting too many specialized kwargs tied to
        # specific commands/subcommands
        # maybe instead of an "args" array plus a bunch of named kwargs,
        # send in a dict that gets passed through tree of argv building logic?
        argv = [op_exe]
        if encoding.lower() != "utf-8":
            global_args.extend(["--encoding", encoding])
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
    def item_generic_argv(cls, op_exe, item_subcommand, sub_cmd_args):
        args = []
        global_args = ["--format", "json"]
        if sub_cmd_args:
            args.extend(sub_cmd_args)
        argv = cls(op_exe, "item", args, subcommand=item_subcommand,
                   global_args=global_args)
        return argv

    @classmethod
    def item_get_argv(cls, op_exe, item_name_or_uuid, vault=None, fields=None):
        sub_cmd_args = [item_name_or_uuid]
        if vault:
            sub_cmd_args.extend(["--vault", vault])

        if fields:
            sub_cmd_args.extend(["--fields", fields])
        argv = cls.item_generic_argv(op_exe, "get", sub_cmd_args)
        return argv

    @classmethod
    def get_totp_argv(cls, op_exe, item_name_or_uuid, vault=None):
        sub_cmd_args = []
        if vault:
            sub_cmd_args.extend(["--vault", vault])

        argv = cls.get_generic_argv(
            op_exe, "totp", item_name_or_uuid, sub_cmd_args)
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
    def document_get_argv(cls, op_exe, document_name_or_uuid, vault=None):
        sub_cmd_args = [document_name_or_uuid]
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
    def vault_get_argv(cls, op_exe, vault_name_or_uuid):
        sub_cmd_args = [vault_name_or_uuid]
        argv = cls.vault_generic_argv(op_exe, "get", sub_cmd_args)
        return argv

    @classmethod
    def normal_signin_argv(cls, op_exe, account_shorthand=None):
        global_args = []
        if account_shorthand:
            global_args = ["--account", account_shorthand]
        argv = ["--raw"]
        return cls(op_exe, "signin", argv, global_args=global_args)

    @classmethod
    def create_item_argv(cls, op_exe, item: OPAbstractItem, item_name: str, vault: str = None, encoding="utf-8"):
        if not item.is_from_template:
            raise OPInvalidItemException(
                f"Attempting to create item using object not from a template: {item_name}")
        template_filename = item.details_secure_tempfile(
            encoding=encoding)

        category = item.category

        argv = [category, "--title", item_name,
                "--template", template_filename]

        # unfortunately the 'op' command can only set one URL
        # so we need to get only the first one
        url = item.first_url()
        url_value = None
        if url:
            url_value = url.url
        if url_value:
            argv.extend(["--url", url_value])

        if vault:
            argv.extend(["--vault", vault])

        return cls(op_exe, "create", argv, subcommand="item")

    @classmethod
    def get_verify_signin_argv(cls, op_exe):
        argv = ["templates"]
        argv_obj = cls(op_exe, "list", argv)
        return argv_obj

    @classmethod
    def cli_version_argv(cls, op_exe):
        args = []
        global_args = ["--version"]
        argv_obj = cls(op_exe, None, args, global_args=global_args)
        return argv_obj

    @classmethod
    def signout_argv(cls, op_exe, account_shorthand: str, session: str, forget=False, uses_bio=False):
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
    def forget_argv(cls, op_exe, account_shorthand):
        forget_args = [account_shorthand]
        argv = cls(op_exe, "forget", forget_args)
        return argv

    @classmethod
    def list_generic_argv(cls, op_exe, list_subcommand, sub_command_args):
        argv = cls(op_exe, "list", sub_command_args,
                   subcommand=list_subcommand)
        return argv

    @classmethod
    def list_items_argv(cls, op_exe, categories=[], include_archive=False, tags=[], vault=None):
        list_items_args = []
        if categories:
            categories_arg = ",".join(categories)
            list_items_args.extend(["--categories", categories_arg])
        if include_archive:
            list_items_args.append("--include-archive")
        if tags:
            tags_args = ",".join(tags)
            list_items_args.extend(["--tags", tags_args])
        if vault:
            list_items_args.extend(["--vault", vault])

        argv = cls.list_generic_argv(op_exe, "items", list_items_args)
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
