from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP
    from ..fixtures.expected_user_data import ExpectedUserData

from pyonepassword.api.exceptions import OPUserGetException

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_user_get_invalid_01(signed_in_op: OP, expected_user_data: ExpectedUserData):
    user_identifier = "No Such User"

    expected = expected_user_data.data_for_user(user_identifier)
    try:
        signed_in_op.user_get(user_identifier)
        assert False, "We should have caught an OPUserGetException"
    except OPUserGetException as e:
        assert e.returncode == expected.returncode
