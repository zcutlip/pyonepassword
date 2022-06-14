from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

from pyonepassword.api.exceptions import (
    OPGroupGetException,
    OPInvalidGroupException
)
from pyonepassword.api.object_types import OPGroup

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_group_get_01(signed_in_op: OP, expected_group_data):
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)
    result = signed_in_op.group_get(group_identifier)
    assert isinstance(result, OPGroup)
    assert result.unique_id == expected.unique_id


def test_group_get_02(signed_in_op: OP, expected_group_data):
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)
    result = signed_in_op.group_get(group_identifier)
    assert isinstance(result, OPGroup)
    assert result.name == expected.name


def test_group_get_03(signed_in_op: OP, expected_group_data):
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)
    result = signed_in_op.group_get(group_identifier)
    assert isinstance(result, OPGroup)
    assert result.description == expected.description


def test_group_get_04(signed_in_op: OP, expected_group_data):
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)
    result = signed_in_op.group_get(group_identifier)
    assert isinstance(result, OPGroup)
    assert result.updated_at == expected.updated_at


def test_group_get_05(signed_in_op: OP, expected_group_data):
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)
    result = signed_in_op.group_get(group_identifier)
    assert isinstance(result, OPGroup)
    assert result.created_at == expected.created_at


def test_group_get_06(signed_in_op: OP, expected_group_data):
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)
    result = signed_in_op.group_get(group_identifier)
    assert isinstance(result, OPGroup)
    assert result.state == expected.state


def test_group_get_07(signed_in_op: OP, expected_group_data):
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)
    result = signed_in_op.group_get(group_identifier)
    assert isinstance(result, OPGroup)
    assert result.type == expected.type


def test_group_get_08(signed_in_op: OP, expected_group_data):
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)
    result = signed_in_op.group_get(group_identifier)
    assert isinstance(result, OPGroup)
    group_perms = result.permissions
    assert isinstance(group_perms, list)
    assert len(group_perms) == len(expected.permissions)
    assert set(group_perms) == set(expected.permissions)


def test_group_get_invalid_01(signed_in_op: OP, expected_group_data):
    group_identifier = "No Such group"
    expected = expected_group_data.data_for_group(group_identifier)
    try:
        signed_in_op.group_get(group_identifier)
        assert False, "Should have caught an OPGroupGetException"
    except OPGroupGetException as e:
        assert e.returncode == expected.returncode


def test_group_get_malformed_json_01(invalid_data):
    malformed_json = invalid_data.data_for_name("malformed-group-json")
    with pytest.raises(OPInvalidGroupException):
        OPGroup(malformed_json)
