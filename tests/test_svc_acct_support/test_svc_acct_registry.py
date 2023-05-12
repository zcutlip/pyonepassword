from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


from pyonepassword._svc_account import (
    SVC_ACCT_CMD_NOT_SUPPORTED,
    SVC_ACCT_INCOMPAT_OPTIONS,
    SVC_ACCT_SUPPORTED,
    OPSvcAcctSupportRegistry
)


def test_svc_acct_command_support_01():
    """
    Create an argv list that is supported but has a required "--vault" option

    Verify the command argv is supported by the service account support registry
    """

    item_get_argv = ['op', '--format', 'json', 'item',
                     'get', 'example item', '--vault', 'test data']
    reg = OPSvcAcctSupportRegistry()
    support = reg.command_supported(item_get_argv)
    assert support["code"] == SVC_ACCT_SUPPORTED


def test_svc_acct_command_support_02():
    """
    Create an argv list using a supported command with subcommands or options

    Verify the command argv is supported by the service account support registry
    """
    item_get_argv = ['op', 'whoami']
    reg = OPSvcAcctSupportRegistry()
    support = reg.command_supported(item_get_argv)
    assert support["code"] == SVC_ACCT_SUPPORTED


def test_svc_acct_command_support_03():
    """
    Create an argv list using a global option with no command or subcommand

    Verify the command argv is supported by the service account support registry
    """
    item_get_argv = ['op', '--version']
    reg = OPSvcAcctSupportRegistry()
    support = reg.command_supported(item_get_argv)
    assert support["code"] == SVC_ACCT_SUPPORTED


def test_svc_acct_command_support_04():
    """
    Create an argv list using an unsupported command

    Verify the command argv is not supported by the service account support registry
    """
    item_get_argv = ['op', 'unknown_command']
    reg = OPSvcAcctSupportRegistry()
    support = reg.command_supported(item_get_argv)
    assert support["code"] == SVC_ACCT_CMD_NOT_SUPPORTED


def test_svc_acct_command_support_05():
    """
    Create an argv list using a supported command and subcommand,
    but missing a required option

    Verify the command argv is not supported by the service account support registry
    """

    # "op item get" is supported but requires a "--vault" argument
    # when used with service accounts
    item_get_argv = ['op', '--format', 'json', 'item', 'get', 'example item']
    reg = OPSvcAcctSupportRegistry()
    support = reg.command_supported(item_get_argv)
    assert support["code"] == SVC_ACCT_INCOMPAT_OPTIONS


def test_svc_acct_command_support_06():
    """
    Create an argv list using a supported command and subcommand,
    but using a prohibited option

    Verify the command argv is not supported by the service account support registry
    """

    # "op vault list" is supported but the "--user" option is prohibited
    # with service accounts
    item_get_argv = ['op', '--format', 'json',
                     'vault', 'list', '--user', "test user"]
    reg = OPSvcAcctSupportRegistry()
    support = reg.command_supported(item_get_argv)
    assert support["code"] == SVC_ACCT_INCOMPAT_OPTIONS
