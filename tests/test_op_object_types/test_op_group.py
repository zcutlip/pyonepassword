from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ..fixtures.expected_group_data import ExpectedGroupData
    from ..fixtures.valid_data import ValidData

from pyonepassword.api.exceptions import OPInvalidGroupException
from pyonepassword.api.object_types import OPGroup

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_op_group_01(valid_data: ValidData, expected_group_data: ExpectedGroupData):
    """
    Create:
        - OPGroup object from "example-login"
    Verify:
        - unique_id property matches expected value
    """
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)

    group_dict = valid_data.data_for_name("example-group")
    result = OPGroup(group_dict)

    assert isinstance(result, OPGroup)
    assert result.unique_id == expected.unique_id


def test_op_group_02(valid_data: ValidData, expected_group_data):
    """
    Create:
        - OPGroup object from "example-login"
    Verify:
        - name property matches expected value
    """
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)

    group_dict = valid_data.data_for_name("example-group")
    result = OPGroup(group_dict)

    assert isinstance(result, OPGroup)
    assert result.name == expected.name


def test_op_group_03(valid_data: ValidData, expected_group_data):
    """
    Create:
        - OPGroup object from "example-login"
    Verify:
        - name property matches expected value
    """
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)

    group_dict = valid_data.data_for_name("example-group")
    result = OPGroup(group_dict)

    assert isinstance(result, OPGroup)
    assert result.description == expected.description


def test_op_group_04(valid_data: ValidData, expected_group_data):
    """
    Create:
        - OPGroup object from "example-login"
    Verify:
        - name property matches expected value
    """
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)

    group_dict = valid_data.data_for_name("example-group")
    result = OPGroup(group_dict)

    assert isinstance(result, OPGroup)
    assert result.updated_at == expected.updated_at


def test_op_group_05(valid_data: ValidData, expected_group_data):
    """
    Create:
        - OPGroup object from "example-login"
    Verify:
        - name property matches expected value
    """
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)

    group_dict = valid_data.data_for_name("example-group")
    result = OPGroup(group_dict)

    assert isinstance(result, OPGroup)
    assert result.created_at == expected.created_at


def test_op_group_06(valid_data: ValidData, expected_group_data):
    """
    Create:
        - OPGroup object from "example-login"
    Verify:
        - name property matches expected value
    """
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)

    group_dict = valid_data.data_for_name("example-group")
    result = OPGroup(group_dict)

    assert isinstance(result, OPGroup)
    assert result.state == expected.state


def test_op_group_07(valid_data: ValidData, expected_group_data):
    """
    Create:
        - OPGroup object from "example-login"
    Verify:
        - name property matches expected value
    """
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)

    group_dict = valid_data.data_for_name("example-group")
    result = OPGroup(group_dict)

    assert isinstance(result, OPGroup)
    assert result.type == expected.type


def test_op_group_08(valid_data: ValidData, expected_group_data):
    """
    Create:
        - OPGroup object from "example-login"
    Verify:
        - name property matches expected value
    """
    group_identifier = "Team Members"
    expected = expected_group_data.data_for_group(group_identifier)

    group_dict = valid_data.data_for_name("example-group")
    result = OPGroup(group_dict)

    assert isinstance(result, OPGroup)
    group_perms = result.permissions
    assert isinstance(group_perms, list)
    assert len(group_perms) == len(expected.permissions)
    assert set(group_perms) == set(expected.permissions)


def test_op_group_malformed_json_01(invalid_data):
    """
    Attempt to create OPGroup object from malformed group JSON

    Verify:
        OPInvalidGroupException is raised
    """
    malformed_json = invalid_data.data_for_name("malformed-group-json")
    with pytest.raises(OPInvalidGroupException):
        OPGroup(malformed_json)
