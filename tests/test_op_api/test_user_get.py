from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP
    from ..fixtures.expected_user_data import ExpectedUserData

from pyonepassword.api.exceptions import OPUserGetException
from pyonepassword.api.object_types import OPUser

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_user_get_01(signed_in_op: OP, expected_user_data):
    # get vault "Test Data"
    user_identifier = "Example User"
    expected = expected_user_data.data_for_user(user_identifier)
    result = signed_in_op.user_get(user_identifier)
    assert isinstance(result, OPUser)
    assert result.unique_id == expected.unique_id


def test_user_get_invalid_01(signed_in_op: OP, expected_user_data: ExpectedUserData):
    user_identifier = "No Such User"

    expected = expected_user_data.data_for_user(user_identifier)
    try:
        signed_in_op.user_get(user_identifier)
        assert False, "We should have caught an OPUserGetException"
    except OPUserGetException as e:
        assert e.returncode == expected.returncode
