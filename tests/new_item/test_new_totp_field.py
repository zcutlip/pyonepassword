from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.exceptions import OPNewTOTPUriException
from pyonepassword.api.object_types import OPNewTOTPField, OPNewTOTPUri

if TYPE_CHECKING:
    from ..fixtures.expected_item_fields import (
        ExpectedItemField,
        ExpectedItemFieldData
    )
    from ..fixtures.invalid_data import InvalidData


def _new_totp_uri():
    issuer = "Example Website"
    account_name = "newuser@website"
    secret = "EPW4UE4E7IKC2QMB"
    new_uri = OPNewTOTPUri(secret, account_name=account_name, issuer=issuer)
    return new_uri


def test_new_totp_uri_01(expected_item_field_data: ExpectedItemFieldData):
    expected_field: ExpectedItemField = expected_item_field_data.data_for_key(
        "example-totp-field")

    expected_uri = expected_field.value

    new_uri = _new_totp_uri()
    assert str(new_uri) == expected_uri


def test_new_totp_uri_02(expected_item_field_data: ExpectedItemFieldData):
    """
    Test OPNewTOTPUri re-padding of non-8-character-aligned secrets during verification

    """
    expected_field: ExpectedItemField = expected_item_field_data.data_for_key(
        "example-totp-field-12-byte-key")
    secret = "36A5PPP5EG3H4JJPGO2A"
    issuer = "Example Company"
    account_name = "newuser_2@website"
    expected_uri = expected_field.value

    new_uri = OPNewTOTPUri(secret, account_name=account_name, issuer=issuer)

    assert len(secret) % 8 != 0
    assert str(new_uri) == expected_uri


def test_new_totp_uri_03(expected_item_field_data: ExpectedItemFieldData):
    """
    Test creating an totp field without an issuer
    """
    expected_field: ExpectedItemField = expected_item_field_data.data_for_key(
        "example-totp-field-no-issuer")
    account_name = "newuser@website"
    secret = "EPW4UE4E7IKC2QMB"
    expected_uri = expected_field.value

    new_uri = OPNewTOTPUri(secret, account_name=account_name)

    assert str(new_uri) == expected_uri


def test_new_totp_uri_invalid_secret_01(invalid_data: InvalidData):
    invalid_secret = invalid_data.data_for_name("invalid_base32_secret")
    issuer = "Example Website"
    account_name = "newuser@website"
    with pytest.raises(OPNewTOTPUriException):
        OPNewTOTPUri(invalid_secret, account_name=account_name, issuer=issuer)


def test_new_totp_field_01(expected_item_field_data: ExpectedItemFieldData):
    expected_field: ExpectedItemField = expected_item_field_data.data_for_key(
        "example-totp-field")
    new_uri = _new_totp_uri()

    totp_field_label = "One-time Password"
    new_field = OPNewTOTPField(totp_field_label, new_uri)

    assert new_field.value == expected_field.value
