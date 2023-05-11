from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


from pyonepassword._svc_account import (
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
