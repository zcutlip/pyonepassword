import enum
from typing import List, Optional


class OPSvcAccountCmdCollisionException(Exception):
    pass


class OPSvcAccountCommandNotSupportedException(Exception):
    pass


class OPSvcAccountSupportedEnum(enum.IntEnum):
    SUPPORTED = 0  # the command is supported by service accounts as-is
    VAULT_REQUIRED = 1  # the command is supported by service accounts,
    # but the required vault argument is missing
    NOT_SUPPORTED = 2  # the command is not supported by service accounts


SVC_ACCT_SUPPORTED = OPSvcAccountSupportedEnum.SUPPORTED
SVC_ACCT_VAULT_REQD = OPSvcAccountSupportedEnum.VAULT_REQUIRED
SVC_ACCT_NOT_SUPPORTED = OPSvcAccountSupportedEnum.NOT_SUPPORTED


class OPSvcAcctSupportRegistry:

    _supported_commands = {}

    @classmethod
    def add_supported_command(cls,
                              command: str,
                              subcommands: Optional[List[str]] = None,
                              vault_required: bool = False):
        collision = True
        if subcommands is None:
            subcommands = []
        command_dict = cls._supported_commands.setdefault(command, dict())

        for sub in subcommands:
            command_dict = command_dict.setdefault(sub, dict())

        if "vault_required" not in command_dict:
            command_dict["vault_required"] = vault_required
            collision = False

        if collision:
            cmd_list = [command]
            cmd_list.extend(subcommands)
            msg = " ".join(cmd_list)
            msg += f" [vault_required={vault_required}]"
            raise OPSvcAccountCmdCollisionException(msg)

    @classmethod
    def command_supported(cls,
                          command: str,
                          subcommands: Optional[List[str]] = None,
                          vault_provided: bool = False) -> OPSvcAccountSupportedEnum:
        # default to unsupported
        supported = SVC_ACCT_NOT_SUPPORTED
        if command is None:
            # command-less options such as --version are always supported
            supported = True
            cmd_dict = None
        else:
            cmd_dict = cls._supported_commands.get(command)

        if cmd_dict:
            for sub in subcommands:
                try:
                    cmd_dict = cmd_dict[sub]
                except KeyError:
                    cmd_dict = {}
                    break

            if "vault_required" in cmd_dict:
                vault_satisfied = False
                if cmd_dict["vault_required"]:
                    vault_satisfied = vault_provided
                else:
                    vault_satisfied = True
                if vault_satisfied:
                    # command is supported as-is
                    supported = SVC_ACCT_SUPPORTED
                else:
                    # command is registered, but vault requirement is not met
                    supported = SVC_ACCT_VAULT_REQD

        return supported


def svc_account_support(command, subcommands=None, vault_required=False):
    OPSvcAcctSupportRegistry.add_supported_command(
        command, subcommands=subcommands, vault_required=vault_required)

    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


def _svc_account_supported(command, subcommand, vault):
    pass


class OPSvcAcctSupported:

    def __init__(self, command: str, subcommand: str, vault_provided: bool = False):
        pass
