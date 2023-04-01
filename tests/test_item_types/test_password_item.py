from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..fixtures.valid_data import ValidData

from pyonepassword.api.object_types import OPPasswordItem


def _lookup_password_data(data, password_identifier: str):
    item = data.data_for_password(password_identifier)
    return item


def test_password_item_010(valid_data: ValidData, expected_item_password_data):
    item_dict = valid_data.data_for_name("example-password")
    password_identifier = "Example Password"

    expected = _lookup_password_data(
        expected_item_password_data, password_identifier)
    result = OPPasswordItem(item_dict)

    assert result.password == expected.password


def test_password_item_020(valid_data: ValidData, expected_item_password_data):
    item_dict = valid_data.data_for_name("example-password")
    password_identifier = "Example Password"

    expected = _lookup_password_data(
        expected_item_password_data, password_identifier)
    result = OPPasswordItem(item_dict)

    assert result.unique_id == expected.unique_id


def test_password_item_030(valid_data: ValidData, expected_item_password_data):
    item_dict = valid_data.data_for_name("example-password")
    password_identifier = "Example Password"

    expected = _lookup_password_data(
        expected_item_password_data, password_identifier)
    result = OPPasswordItem(item_dict)

    assert result.title == expected.title


def test_password_item_040(valid_data: ValidData, expected_item_password_data):
    item_dict = valid_data.data_for_name("example-password")
    password_identifier = "Example Password"

    expected = _lookup_password_data(
        expected_item_password_data, password_identifier)
    result = OPPasswordItem(item_dict)

    assert result.created_at == expected.created_at


def test_password_item_050(valid_data: ValidData, expected_item_password_data):
    item_dict = valid_data.data_for_name("example-password")
    password_identifier = "Example Password"

    expected = _lookup_password_data(
        expected_item_password_data, password_identifier)
    result = OPPasswordItem(item_dict)

    assert result.updated_at == expected.updated_at


def test_password_item_060(valid_data: ValidData, expected_item_password_data):
    item_dict = valid_data.data_for_name("example-password")
    password_identifier = "Example Password"

    expected = _lookup_password_data(
        expected_item_password_data, password_identifier)
    result = OPPasswordItem(item_dict)

    assert result.last_edited_by == expected.last_edited_by


def test_password_item_070(valid_data: ValidData, expected_item_password_data):
    item_dict = valid_data.data_for_name("example-password")
    password_identifier = "Example Password"

    expected = _lookup_password_data(
        expected_item_password_data, password_identifier)
    result = OPPasswordItem(item_dict)

    assert result.vault_id == expected.vault_id
