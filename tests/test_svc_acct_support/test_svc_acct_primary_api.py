"""
Test primary API when a service account is in use

Some API methods should work as is, some require specific options,
and some prohibit specific options.
"""
from __future__ import annotations

# inspect, re required for checking docstrings
import inspect
import re

import pytest

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


def test_svc_account_primary_api_docstrings():
    """
    Inspect each non-private instance or class method in the OP class

    Verify:
        Each method's docstring contains at least the following section documenting service accounts:
        Service Account Support
        -----------------------
    """
    # regex where '.' will match newlines
    svc_account_string_re = re.compile(
        r"Service Account Support.\s+-----------------------", re.DOTALL)

    # get all class and instance methods
    api_method_dict = {fn_name: attr for fn_name, attr in vars(
        OP).items() if inspect.isfunction(attr) or isinstance(attr, classmethod)}

    # filter out "private" methods
    api_method_dict = {fn_name: attr for fn_name,
                       attr in api_method_dict.items() if not fn_name.startswith("_")}

    failures = []
    for meth_name, method_obj in api_method_dict.items():
        matches = re.search(svc_account_string_re, method_obj.__doc__)
        if not matches:
            # we didn't find service account support in the docstring
            failures.append(f"OP.{meth_name}()")
        else:
            # we found mention of service account support but it was incomplete or not formatted properly
            if len(matches[0].splitlines()) != 2:
                failures.append(f"OP.{meth_name}()")

    # len(failures) should == 0
    # if not generate failure message from list of failures
    assert len(
        failures) == 0, f"API methods without documented service account support: {failures}"
