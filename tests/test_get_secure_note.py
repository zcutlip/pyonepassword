import pytest
from pyonepassword import OP, OPSecureNoteItem


def _lookup_note_data(data, note_identifier: str):
    item = data.data_for_note(note_identifier)
    return item


@pytest.mark.parametrize("note_identifier,vault",
                         [("Example Secure Note", "Test Data"),
                          ("Example Secure Note 2", None),
                          ("t4gp6e7s6xtsiu35xq5cewxqpi", None)])
def test_get_secure_note_item_01(signed_in_op: OP, expected_secure_note_item_data, note_identifier, vault):
    expected = _lookup_note_data(
        expected_secure_note_item_data, note_identifier)
    result: OPSecureNoteItem = signed_in_op.get_item(
        note_identifier, vault=vault)
    assert isinstance(result, OPSecureNoteItem)
    assert result.note_text == expected.note_text
    assert result.uuid == expected.uuid
    assert result.title == expected.title
    assert result.created_at == expected.created_at
    assert result.updated_at == expected.updated_at
    assert result.changer_uuid == expected.changer_uuid
    assert result.vault_uuid == expected.vault_uuid
    assert result.trashed == expected.trashed
