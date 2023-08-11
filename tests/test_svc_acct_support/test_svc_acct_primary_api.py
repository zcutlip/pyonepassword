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
    OPItemGetException,
    OPRevokedSvcAcctTokenException,
    OPSvcAcctCommandNotSupportedException
)
from pyonepassword.api.object_types import OPLoginItem


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_env")
def test_svc_acct_item_get_010(signed_in_op_svc_acct: OP):
    """
    Service account command test: "op item get --vault"

    Set service account token via fixture
    call OP.item_get() with required vault argument

    Verify the call succeeds
    """
    item_name = "Example Login 1"
    vault = "Test Data"

    result = signed_in_op_svc_acct.item_get(item_name, vault=vault)

    assert isinstance(result, OPLoginItem)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_env")
def test_svc_acct_item_get_020(signed_in_op_svc_acct: OP):
    """
    Service account command test: "op item get"

    This excercises the supported commands missing required arguments code paths

    Set service account token via fixture
    call OP.item_get() without required vault argument

    Verify the call fails with OPSvcAcctCommandNotSupportedException
    """
    item_name = "Example Login 1"
    with pytest.raises(OPSvcAcctCommandNotSupportedException):
        signed_in_op_svc_acct.item_get(item_name)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_env")
def test_svc_acct_item_get_025(signed_in_op_svc_acct: OP):
    """
    Service account command test: "op item get"

    Set service account token via fixture
    call OP.item_get() with an unauthorized vault argument

    Verify the call fails with OPItemGetException
    """
    item_name = "Example Login 1"
    # unauthorized vault
    vault = "Local"
    with pytest.raises(OPItemGetException):
        signed_in_op_svc_acct.item_get(item_name, vault=vault)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_account_revoked_env")
def test_svc_acct_item_get_027(signed_in_op_svc_acct: OP):
    """
    Service account command test: "op item get"

    Set revoked service account token via fixture
    call OP.item_get() with appropriate arguments

    Verify the call fails with OPRevokedSvcAcctTokenException
    """
    item_name = "Example Login 1"
    vault = "Test Data"

    with pytest.raises(OPRevokedSvcAcctTokenException):
        signed_in_op_svc_acct.item_get(item_name, vault=vault)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_env")
def test_svc_acct_vault_list_030(signed_in_op_svc_acct: OP):
    """
    """
    result = signed_in_op_svc_acct.vault_list()
    assert isinstance(result, OPVaultDescriptorList)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_svc_acct_env")
def test_svc_acct_vault_list_040(signed_in_op_svc_acct: OP):
    """
    Service account command test: "op vault list --group 'Team Members'"

    This excercises the supported commands with prohibited arguments code paths

    Set service account token via fixture
    call OP.vault_list() with the prohibited group argument

    Verify the call fails with OPSvcAcctCommandNotSupportedException
    """
    group = "Team Members"

    with pytest.raises(OPSvcAcctCommandNotSupportedException):
        signed_in_op_svc_acct.vault_list(group_name_or_id=group)


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
    op_vars = vars(OP)
    api_method_dict = {}
    for fn_name, attr in op_vars.items():
        if isinstance(attr, classmethod):
            # we should be able to use attr directly
            # but for some reason this doesn't always have the proper __doc__
            api_method_dict[fn_name] = getattr(OP, fn_name)
        elif inspect.isfunction(attr):
            api_method_dict[fn_name] = attr

    # filter out "private" methods
    api_method_dict = {fn_name: attr for fn_name,
                       attr in api_method_dict.items() if not fn_name.startswith("_")}

    failures = []
    for meth_name, method_obj in api_method_dict.items():
        if not method_obj.__doc__:
            # no docstring at all
            failures.append(f"OP.{meth_name}()")
        else:
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
