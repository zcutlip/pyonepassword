from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ..fixtures.valid_data import ValidData

from pyonepassword.api.object_types import OPSecureNoteItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_secure_note_item_010(valid_data: ValidData, expected_secure_note_item_data):
    expected = expected_secure_note_item_data.data_for_note(
        "Example Secure Note")
    item_dict = valid_data.data_for_name("example-secure-note")
    result = OPSecureNoteItem(item_dict)

    assert result.note_text == expected.note_text


def test_secure_note_item_020(valid_data: ValidData, expected_secure_note_item_data):
    expected = expected_secure_note_item_data.data_for_note(
        "Example Secure Note")
    item_dict = valid_data.data_for_name("example-secure-note")
    result = OPSecureNoteItem(item_dict)
    assert result.unique_id == expected.unique_id


def test_secure_note_item_030(valid_data: ValidData, expected_secure_note_item_data):
    expected = expected_secure_note_item_data.data_for_note(
        "Example Secure Note")
    item_dict = valid_data.data_for_name("example-secure-note")
    result = OPSecureNoteItem(item_dict)
    assert result.title == expected.title


def test_secure_note_item_040(valid_data: ValidData, expected_secure_note_item_data):
    expected = expected_secure_note_item_data.data_for_note(
        "Example Secure Note")
    item_dict = valid_data.data_for_name("example-secure-note")
    result = OPSecureNoteItem(item_dict)
    assert result.created_at == expected.created_at


def test_secure_note_item_050(valid_data: ValidData, expected_secure_note_item_data):
    expected = expected_secure_note_item_data.data_for_note(
        "Example Secure Note")
    item_dict = valid_data.data_for_name("example-secure-note")
    result = OPSecureNoteItem(item_dict)
    assert result.updated_at == expected.updated_at


def test_secure_note_item_060(valid_data: ValidData, expected_secure_note_item_data):
    expected = expected_secure_note_item_data.data_for_note(
        "Example Secure Note")
    item_dict = valid_data.data_for_name("example-secure-note")
    result = OPSecureNoteItem(item_dict)
    assert result.last_edited_by == expected.last_edited_by


def test_secure_note_item_070(valid_data: ValidData, expected_secure_note_item_data):
    expected = expected_secure_note_item_data.data_for_note(
        "Example Secure Note")
    item_dict = valid_data.data_for_name("example-secure-note")
    result = OPSecureNoteItem(item_dict)
    assert result.vault_id == expected.vault_id
