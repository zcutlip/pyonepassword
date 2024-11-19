from __future__ import annotations

from typing import TYPE_CHECKING

# import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

    from ....fixtures.expected_item_share_data import (
        ExpectedItemShare,
        ExpectedItemShareData
    )


def test_item_share_010(signed_in_op: OP, expected_item_share_data: ExpectedItemShareData):
    """
    Test: OP.item_share() with the following parameter
        - Item name as item_identifier
    Verify:
        - The item share URL matches the expected URL
    """
    item_key = "item-share-example-login-22-1"
    expected_item_share: ExpectedItemShare
    expected_item_share = expected_item_share_data.data_for_key(item_key)

    item_name = "Example Login Item 22"
    assert expected_item_share.item_identifier == item_name

    share_url = signed_in_op.item_share(item_name)

    assert share_url == expected_item_share.url


def test_item_share_020(signed_in_op: OP, expected_item_share_data: ExpectedItemShareData):
    """
    Test: OP.item_share() with the following parameters
        - Item name as item_identifier
        - vault= kwarg
    Verify:
        - The item share URL matches the expected URL
    """
    item_key = "item-share-example-login-22-2"
    expected_item_share: ExpectedItemShare
    expected_item_share = expected_item_share_data.data_for_key(item_key)

    item_name = "Example Login Item 22"
    vault = "Test Data 1"
    assert expected_item_share.item_identifier == item_name

    share_url = signed_in_op.item_share(item_name, vault=vault)

    assert share_url == expected_item_share.url


def test_item_share_030(signed_in_op: OP, expected_item_share_data: ExpectedItemShareData):
    """
    Test: OP.item_share() with the following parameters
        - Item name as item_identifier
        - Vault kwarg
        - List of two email strings as emails= kwarg
    Verify:
        - The item share URL matches the expected URL
    """
    item_key = "item-share-example-login-22-3"
    expected_item_share: ExpectedItemShare
    expected_item_share = expected_item_share_data.data_for_key(item_key)

    item_name = "Example Login Item 22"
    vault = "Test Data 1"
    emails = "user_1@example.com,user_2@example.com".split(",")
    assert expected_item_share.item_identifier == item_name

    share_url = signed_in_op.item_share(item_name, vault=vault, emails=emails)

    assert share_url == expected_item_share.url


def test_item_share_035(signed_in_op: OP, expected_item_share_data: ExpectedItemShareData):
    """
    Test: OP.item_share() with the following parameters
        - Item name as item_identifier
        - Vault kwarg
        - Single email string as emails= kwarg
    Verify:
        - The item share URL matches the expected URL
    """
    item_key = "item-share-example-login-22-3a"
    expected_item_share: ExpectedItemShare
    expected_item_share = expected_item_share_data.data_for_key(item_key)

    item_name = "Example Login Item 22"
    vault = "Test Data 1"
    email = "user_1@example.com"
    assert expected_item_share.item_identifier == item_name

    share_url = signed_in_op.item_share(item_name, vault=vault, emails=email)

    assert share_url == expected_item_share.url


def test_item_share_036(signed_in_op: OP, expected_item_share_data: ExpectedItemShareData):
    """
    Test: OP.item_share() with the following parameters
        - Item name as item_identifier
        - Vault kwarg
        - List of one email string as emails= kwarg
    Verify:
        - The item share URL matches the expected URL
    """
    item_key = "item-share-example-login-22-3a"
    expected_item_share: ExpectedItemShare
    expected_item_share = expected_item_share_data.data_for_key(item_key)

    item_name = "Example Login Item 22"
    vault = "Test Data 1"
    email = ["user_1@example.com"]
    assert expected_item_share.item_identifier == item_name

    share_url = signed_in_op.item_share(item_name, vault=vault, emails=email)

    assert share_url == expected_item_share.url


def test_item_share_040(signed_in_op: OP, expected_item_share_data: ExpectedItemShareData):
    """
    Test: OP.item_share() with the following parameters
        - Item name as item_identifier
        - Vault kwarg
        - List of two email strings as emails= kwarg
        - "2d" as expires_in= kwarg
    Verify:
        - The item share URL matches the expected URL
    """
    item_key = "item-share-example-login-22-4"
    expected_item_share: ExpectedItemShare
    expected_item_share = expected_item_share_data.data_for_key(item_key)

    item_name = "Example Login Item 22"
    vault = "Test Data 1"
    emails = "user_1@example.com,user_2@example.com".split(",")
    expires_in = "2d"
    assert expected_item_share.item_identifier == item_name

    share_url = signed_in_op.item_share(
        item_name, vault=vault, emails=emails, expires_in=expires_in)

    assert share_url == expected_item_share.url
