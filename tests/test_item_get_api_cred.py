# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import pytest

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from .fixtures.expected_api_credential_data import ExpectedAPICredential, ExpectedAPICredentialData
    from pyonepassword import OP

from pyonepassword.api.object_types import OPAPICredentialItem

pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_item_get_api_cred_01(signed_in_op: OP, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    result: OPAPICredentialItem
    expected: ExpectedAPICredential

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = signed_in_op.item_get(api_cred_name, vault="Test Data")

    assert isinstance(result, OPAPICredentialItem)
    assert result.unique_id == expected.unique_id


def test_item_get_api_cred_02(signed_in_op: OP, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    result: OPAPICredentialItem
    expected: ExpectedAPICredential

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = signed_in_op.item_get(api_cred_name, vault="Test Data")

    assert isinstance(result, OPAPICredentialItem)
    assert result.username == expected.username


def test_item_get_api_cred_03(signed_in_op: OP, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    result: OPAPICredentialItem
    expected: ExpectedAPICredential

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = signed_in_op.item_get(api_cred_name, vault="Test Data")

    assert isinstance(result, OPAPICredentialItem)
    assert result.credential == expected.credential


def test_item_get_api_cred_04(signed_in_op: OP, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    result: OPAPICredentialItem
    expected: ExpectedAPICredential

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = signed_in_op.item_get(api_cred_name, vault="Test Data")

    assert isinstance(result, OPAPICredentialItem)
    assert result.credential == expected.credential


def test_item_get_api_cred_05(signed_in_op: OP, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    result: OPAPICredentialItem
    expected: ExpectedAPICredential

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = signed_in_op.item_get(api_cred_name, vault="Test Data")

    assert isinstance(result, OPAPICredentialItem)
    assert result.type == expected.type


def test_item_get_api_cred_06(signed_in_op: OP, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    result: OPAPICredentialItem
    expected: ExpectedAPICredential

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = signed_in_op.item_get(api_cred_name, vault="Test Data")

    assert isinstance(result, OPAPICredentialItem)
    assert result.filename == expected.filename


def test_item_get_api_cred_07(signed_in_op: OP, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    result: OPAPICredentialItem
    expected: ExpectedAPICredential

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = signed_in_op.item_get(api_cred_name, vault="Test Data")

    assert isinstance(result, OPAPICredentialItem)
    valid_from = result.valid_from
    assert isinstance(valid_from, date)
    assert valid_from == expected.valid_from


def test_item_get_api_cred_08(signed_in_op: OP, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    result: OPAPICredentialItem
    expected: ExpectedAPICredential

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = signed_in_op.item_get(api_cred_name, vault="Test Data")

    assert isinstance(result, OPAPICredentialItem)
    expires = result.expires
    assert isinstance(expires, date)
    assert expires == expected.expires


def test_item_get_api_cred_09(signed_in_op: OP, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    result: OPAPICredentialItem
    expected: ExpectedAPICredential

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = signed_in_op.item_get(api_cred_name, vault="Test Data")

    assert isinstance(result, OPAPICredentialItem)
    assert result.hostname == expected.hostname
