# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from ..fixtures.expected_api_credential_data import ExpectedAPICredentialData
    from ..fixtures.valid_data import ValidData

from pyonepassword.api.object_types import OPAPICredentialItem


def test_api_credential_item_010(valid_data: ValidData, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    item_dict = valid_data.data_for_name("example-api-credential")

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = OPAPICredentialItem(item_dict)

    assert isinstance(result, OPAPICredentialItem)
    assert result.unique_id == expected.unique_id


def test_api_credential_item_020(valid_data: ValidData, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    item_dict = valid_data.data_for_name("example-api-credential")

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = OPAPICredentialItem(item_dict)

    assert isinstance(result, OPAPICredentialItem)
    assert result.username == expected.username


def test_api_credential_item_030(valid_data: ValidData, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    item_dict = valid_data.data_for_name("example-api-credential")

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = OPAPICredentialItem(item_dict)

    assert isinstance(result, OPAPICredentialItem)
    assert result.credential == expected.credential


def test_api_credential_item_040(valid_data: ValidData, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    item_dict = valid_data.data_for_name("example-api-credential")

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = OPAPICredentialItem(item_dict)

    assert isinstance(result, OPAPICredentialItem)
    assert result.credential == expected.credential


def test_api_credential_item_050(valid_data: ValidData, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    item_dict = valid_data.data_for_name("example-api-credential")

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = OPAPICredentialItem(item_dict)

    assert isinstance(result, OPAPICredentialItem)
    assert result.type == expected.type


def test_api_credential_item_060(valid_data: ValidData, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    item_dict = valid_data.data_for_name("example-api-credential")

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = OPAPICredentialItem(item_dict)

    assert isinstance(result, OPAPICredentialItem)
    assert result.filename == expected.filename


def test_api_credential_item_070(valid_data: ValidData, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    item_dict = valid_data.data_for_name("example-api-credential")

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = OPAPICredentialItem(item_dict)

    assert isinstance(result, OPAPICredentialItem)
    valid_from = result.valid_from
    assert isinstance(valid_from, date)
    assert valid_from == expected.valid_from


def test_api_credential_item_080(valid_data: ValidData, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    item_dict = valid_data.data_for_name("example-api-credential")

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = OPAPICredentialItem(item_dict)

    assert isinstance(result, OPAPICredentialItem)
    expires = result.expires
    assert isinstance(expires, date)
    assert expires == expected.expires


def test_api_credential_item_090(valid_data: ValidData, expected_api_credential_data: ExpectedAPICredentialData):
    api_cred_name = "Example API Credential"
    item_dict = valid_data.data_for_name("example-api-credential")

    expected = expected_api_credential_data.api_cred_data_for_login(
        api_cred_name)

    result = OPAPICredentialItem(item_dict)

    assert isinstance(result, OPAPICredentialItem)
    assert result.hostname == expected.hostname
