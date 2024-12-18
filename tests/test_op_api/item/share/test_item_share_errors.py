from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.exceptions import OPItemShareException

if TYPE_CHECKING:
    from pyonepassword import OP


def test_item_share_invalid_expires_010(signed_in_op: OP):
    """
    Test: OP.item_share() with an invalid "expires-in" string
        - Invalid "5q" string as expires_in kwarg
        - Valid values for item_identifier, emails, & vault
    Verify:
        - OPItemShareException is raised
    """

    item_name = "Example Login Item 22"
    expires_in = "5q"
    email = "user_1@example.com"
    vault = "Test Data 1"
    with pytest.raises(OPItemShareException):
        signed_in_op.item_share(item_name, emails=email,
                                expires_in=expires_in, vault=vault)


def test_item_share_invalid_expires_020(signed_in_op: OP):
    """
    Test: OP.item_share() with an invalid "expires-in" string
        - Invalid "banana" string as expires_in kwarg
        - Valid values for item_identifier, emails, & vault
    Verify:
        - OPItemShareException is raised

    NOTE: The error message for a completely invalid string such as
        this is different than the error for a number+leter like "5q"
    """
    item_name = "Example Login Item 22"
    expires_in = "banana"
    email = "user_1@example.com"
    vault = "Test Data 1"
    with pytest.raises(OPItemShareException):
        signed_in_op.item_share(item_name, emails=email,
                                expires_in=expires_in, vault=vault)


def test_item_share_invalid_email_030(signed_in_op: OP):
    """
    Test: OP.item_share() with an invalid email string
        - Invalid "foo" string as emails= kwarg
        - Valid values for item_identifier & vault
    Verify:
        - OPItemShareException is raised

    NOTE: Different malformed email addresses generate different error messages and return codes
    """
    item_name = "Example Login Item 22"
    email = "foo"
    vault = "Test Data 1"

    with pytest.raises(OPItemShareException):
        signed_in_op.item_share(item_name, emails=email, vault=vault)


def test_item_share_invalid_email_040(signed_in_op: OP):
    """
    Test: OP.item_share() with an invalid email string
        - Invalid "foo@foobar." string as emails= kwarg
        - Valid values for item_identifier & vault
    Verify:
        - OPItemShareException is raised

    NOTE: Different malformed email addresses generate different error messages and return codes
    """
    item_name = "Example Login Item 22"
    email = "foo@foobar."
    vault = "Test Data 1"

    with pytest.raises(OPItemShareException):
        signed_in_op.item_share(item_name, emails=email, vault=vault)
