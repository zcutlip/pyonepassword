import enum
import json
from typing import Any, Dict, List, NamedTuple, Optional, Set

from pysingleton import PySingleton  # type: ignore

from . import data
from .pkg_resources import data_location_as_path

OptionalStrList = Optional[List[str]]


class OPSvcAcctCommandNotSupportedException(Exception):
    pass


class OPSvcAcctSupportedEnum(enum.IntEnum):
    NOT_VALIDATED = -1
    SUPPORTED = 0  # the command is supported by service accounts as-is
    INCOMPAT_OPTIONS = 1  # the command is supported by service accounts,
    # but the required vault argument is missing
    NOT_SUPPORTED = 2  # the command is not supported by service accounts


SVC_ACCT_SUPPORTED = OPSvcAcctSupportedEnum.SUPPORTED
SVC_ACCT_INCOMPAT_OPTIONS = OPSvcAcctSupportedEnum.INCOMPAT_OPTIONS
SVC_ACCT_CMD_NOT_SUPPORTED = OPSvcAcctSupportedEnum.NOT_SUPPORTED
_SVC_ACCT_CMD_NOT_VALIDATED = OPSvcAcctSupportedEnum.NOT_VALIDATED


class OPSvcAcctSupportCode(NamedTuple):
    code: OPSvcAcctSupportedEnum
    msg: Optional[str]


class _CmdSpec(dict):

    def __init__(self, cmd_dict):
        super().__init__(cmd_dict)

    @property
    def command_name(self) -> str:
        return self["meta"]["command_name"]

    def _main_command_dict(self) -> Dict:
        # Return command dict for the top-level command
        # if there is one
        # else empty dict
        cmd_dict = self.get("cmd_dict", {})
        return cmd_dict

    def command_lookup(self, subcommand_list: OptionalStrList = None):
        # subcommand_list, if provided, is a subcommand chain of one or more items
        # e.g, the "op item" command has the following subcommands (not exhaustive):
        # - get (e.g., op item get <item>)
        # - template list (e.g., op item template list <item_type>)
        subcmd_dict = self.get("subcommands", {})
        found: Dict[Any, Any] = {}

        if subcommand_list:
            # if we were given a subcommand list with one or more items
            # then try to find the command dict for the subcommand chain
            for subcmd in subcommand_list:
                subcmd_dict = subcmd_dict.get(subcmd, {})
                if "has_arg" in subcmd_dict:
                    # check if current subcommand is the most deeply nested,
                    # if so, the next entry in our list may be a positional
                    # argument argument and not another subcommand,
                    # so stop processing here
                    found = subcmd_dict
                    break
        else:
            # there was no subcommand list (e.g., in the case of op whoami)
            # so get the top-level command dict
            found = self._main_command_dict()

        return found


# Make the registry a singleton to avoid
# loading all the JSON files from disk each time
# it gets instantiated
class OPSvcAcctSupportRegistry(metaclass=PySingleton):
    # This allows the instance to be freed & reinitialized
    # once the last reference released
    _PYSINGLETON_WEAKREF = True
    """
    A registry of supported commands, subcommands, and required & prohibited options
    in the context of service accounts
    """

    def __init__(self):
        self._supported_commands = {}
        # data_location_as_path() satisfies mypy
        # by returning a Path instead of a Traversable
        data_path = data_location_as_path(data, data.SVC_ACCOUNT_COMMANDS)

        for json_file in data_path.glob("*.json"):
            cmd_dict = json.load(open(json_file, "r"))
            self._process(cmd_dict)

    def _process(self, cmd_dict: Dict):
        cmd_spec = _CmdSpec(cmd_dict)
        cmd = cmd_spec.command_name
        self._supported_commands[cmd] = cmd_spec

    def command_supported(self, _argv: List[str]) -> OPSvcAcctSupportCode:
        # This function is much more complex than I'd like, but most of the complexity is
        # around building necessary context for a meaningful exception message

        _support_code = _SVC_ACCT_CMD_NOT_VALIDATED
        _support_msg: str = None

        # for testing of all required options are provided
        # and for generating error message
        reqd_opt_diff: Set[str] = set()
        required_opt_satified = False
        # for generating error message if any prohibted options are found
        prohib_opt_diff: Set[str] = set()
        prohibited_opt_satisfied = False
        # copy argv so we don't modify the original
        argv_list: List[str] = list(_argv)
        # [op_exe, [global options, ...], [subcommands, ...], [--sub-cmd-options, ...]]
        cmd_spec: _CmdSpec

        # pop argv[0], the op exe path
        argv_list.pop(0)

        # the following global options each take an argument
        # e.g., "--format json"
        global_options_with_args = ["--format",
                                    "--encoding", "--session", "--config"]

        # pop global options
        while argv_list and argv_list[0].startswith("--"):
            arg = argv_list.pop(0)
            # does the option have an argument that also
            # needs to be popped?
            # e.g., if we popped "--format", we also
            # need to pop its argument, "json"
            if arg in global_options_with_args:
                argv_list.pop(0)

        # get primary command
        command = None
        if argv_list:
            command = argv_list.pop(0)

        # build subcommands:
        subcommands = []
        while argv_list and not argv_list[0].startswith("--"):
            subcommands.append(argv_list.pop(0))

        # build subcommand option list
        subcmd_options = []
        while argv_list:
            # pop off all subcommand options, ignoring option-arguments
            # e.g, save "--vault", but skip argument "Test Data"
            option = argv_list.pop(0)
            if option.startswith("--"):
                subcmd_options.append(option)

        if command is None:
            # command-less options such as --version are always supported
            _support_code = SVC_ACCT_SUPPORTED
            _support_msg = None
            cmd_spec = None
            required_opt_satified = True
            prohibited_opt_satisfied = True
        else:
            cmd_spec = self._supported_commands.get(command)

        cmd_dict = {}
        if cmd_spec:
            cmd_dict = cmd_spec.command_lookup(subcommand_list=subcommands)

        # if we either failed to find a command spec or
        # we found a command spec but not a subcommand dictionary
        # then command is not supported
        _cmd_not_found = command is not None and cmd_spec is None
        if (cmd_spec and not cmd_dict) or _cmd_not_found:
            _support_msg = f"Command or subcommand not supported: [{command} {' '.join(subcommands)}]"
            _support_code = SVC_ACCT_CMD_NOT_SUPPORTED

        if cmd_dict and _support_code == _SVC_ACCT_CMD_NOT_VALIDATED:
            required_options = set(cmd_dict["required_options"])

            # how many required options remain after we mask out
            # the provided options? Hopefully none
            # we use the diff for two purposes:
            # 1. to test if any required options were omitted
            # 2. to generate a meaninful error message if needed
            reqd_opt_diff = required_options - set(subcmd_options)

            if not reqd_opt_diff:
                # all required options were in use, so we're good here
                required_opt_satified = True
            else:
                _support_code = SVC_ACCT_INCOMPAT_OPTIONS

            prohibited_options = set(cmd_dict["prohibited_options"])

            # how many probited options remain after we mask out
            # the provided options? Hopefully all of them
            remaining = prohibited_options - set(subcmd_options)

            if remaining == prohibited_options:
                # didn't use any prohbited options, so we're good here
                prohibited_opt_satisfied = True
            else:
                # which prohibted options were actually used?
                # we need this to generate the error message
                prohib_opt_diff = prohibited_options - remaining
                _support_code = SVC_ACCT_INCOMPAT_OPTIONS

            if required_opt_satified and prohibited_opt_satisfied:
                # if both
                _support_code = SVC_ACCT_SUPPORTED

        if _support_code == SVC_ACCT_INCOMPAT_OPTIONS:
            _support_msg = ""
            if not required_opt_satified:
                _support_msg += f"Required options not provided: [{','.join(list(reqd_opt_diff))}]"

            if not prohibited_opt_satisfied:
                _support_msg += f" Prohibited options found: [{','.join(list(prohib_opt_diff))}]"

            _support_msg = _support_msg.lstrip()

        if _support_code == _SVC_ACCT_CMD_NOT_VALIDATED:  # pragma: no cover
            # something's gone wrong if we reach this point
            raise Exception("Failed to validate service account compatibility")

        supported = OPSvcAcctSupportCode(_support_code, _support_msg)

        return supported
