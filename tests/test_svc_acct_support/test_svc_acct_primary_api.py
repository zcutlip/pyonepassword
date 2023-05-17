"""
Test primary API when a service account is in use

Some API methods should work as is, some require specific options,
and some prohibit specific options.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword.api.descriptor_types import OPVaultDescriptorList
from pyonepassword.api.exceptions import (
    OPSvcAccountCommandNotSupportedException
)
from pyonepassword.api.object_types import OPLoginItem


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_env")
def test_svc_acct_item_get_01(signed_in_op: OP):
    """
    Service account command test: "op item get --vault"

    Set service account token via fixture
    call OP.item_get() with required vault argument

    Verify the call succeeds
    """
    item_name = "Example Login 1"
    vault = "Test Data"

    result = signed_in_op.item_get(item_name, vault=vault)

    assert isinstance(result, OPLoginItem)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_env")
def test_svc_acct_item_get_02(signed_in_op: OP):
    """
    Service account command test: "op item get"

    This excercises the supported commands missing required arguments code paths

    Set service account token via fixture
    call OP.item_get() without required vault argument

    Verify the call fails with OPSvcAccountCommandNotSupportedException
    """
    item_name = "Example Login 1"
    with pytest.raises(OPSvcAccountCommandNotSupportedException):
        signed_in_op.item_get(item_name)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_env")
def test_svc_acct_item_get_03(signed_in_op: OP):
    """
    """
    result = signed_in_op.vault_list()
    assert isinstance(result, OPVaultDescriptorList)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_env")
def test_svc_acct_item_get_04(signed_in_op: OP):
    """
    Service account command test: "op vault list --group 'Team Members'"

    This excercises the supported commands with prohibited arguments code paths

    Set service account token via fixture
    call OP.vault_list() with the prohibited group argument

    Verify the call fails with OPSvcAccountCommandNotSupportedException
    """
    group = "Team Members"

    with pytest.raises(OPSvcAccountCommandNotSupportedException):
        signed_in_op.vault_list(group_name_or_id=group)
