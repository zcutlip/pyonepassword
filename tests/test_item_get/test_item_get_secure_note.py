from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword.api.exceptions import OPItemGetException

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _lookup_note_data(data, note_identifier: str):
    item = data.data_for_note(note_identifier)
    return item


@pytest.mark.parametrize("invalid_note,vault",
                         [("Example Secure Note 3", None),
                          ("Example Secure Note 4", "Test Data")])
def test_item_get_invalid_secure_note_02(signed_in_op: OP, expected_secure_note_item_data, invalid_note, vault):
    exception_class = OPItemGetException
    expected = _lookup_note_data(
        expected_secure_note_item_data, invalid_note)
    try:
        signed_in_op.item_get(invalid_note, vault=vault)
        assert False, f"We should have caught {exception_class.__name__}"
    except exception_class as e:
        assert e.returncode == expected.returncode
