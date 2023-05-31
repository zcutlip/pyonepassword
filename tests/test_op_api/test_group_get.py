from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword.api.exceptions import OPGroupGetException
from pyonepassword.api.object_types import OPGroup

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_group_get_01(signed_in_op: OP, expected_group_data):
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)
    result = signed_in_op.group_get(group_identifier)
    assert isinstance(result, OPGroup)
    assert result.unique_id == expected.unique_id


def test_group_get_invalid_01(signed_in_op: OP, expected_group_data):
    group_identifier = "No Such group"
    expected = expected_group_data.data_for_group(group_identifier)
    try:
        signed_in_op.group_get(group_identifier)
        assert False, "Should have caught an OPGroupGetException"
    except OPGroupGetException as e:
        assert e.returncode == expected.returncode
