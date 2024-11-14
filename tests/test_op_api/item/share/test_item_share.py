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
    item_key = "item-share-example-login-22-1"
    expected_item_share: ExpectedItemShare
    expected_item_share = expected_item_share_data.data_for_key(item_key)

    item_name = "Example Login Item 22"
    assert expected_item_share.item_identifier == item_name

    share_url = signed_in_op.item_share(item_name)

    assert share_url == expected_item_share.url


def test_item_share_020(signed_in_op: OP, expected_item_share_data: ExpectedItemShareData):
    item_key = "item-share-example-login-22-2"
    expected_item_share: ExpectedItemShare
    expected_item_share = expected_item_share_data.data_for_key(item_key)

    item_name = "Example Login Item 22"
    vault = "Test Data 1"
    assert expected_item_share.item_identifier == item_name

    share_url = signed_in_op.item_share(item_name, vault=vault)

    assert share_url == expected_item_share.url


def test_item_share_030(signed_in_op: OP, expected_item_share_data: ExpectedItemShareData):
    item_key = "item-share-example-login-22-3"
    expected_item_share: ExpectedItemShare
    expected_item_share = expected_item_share_data.data_for_key(item_key)

    item_name = "Example Login Item 22"
    vault = "Test Data 1"
    emails = "user_1@example.com,user_2@example.com".split(",")
    assert expected_item_share.item_identifier == item_name

    share_url = signed_in_op.item_share(item_name, vault=vault, emails=emails)

    assert share_url == expected_item_share.url


def test_item_share_040(signed_in_op: OP, expected_item_share_data: ExpectedItemShareData):
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
