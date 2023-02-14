"""
Test cases for the 'relaxed_validation' kwarg to OP 'item get' methods
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyonepassword import OP

    from ..fixtures.expected_login import ExpectedLogin, ExpectedLoginItemData

from pyonepassword.api.exceptions import OPSectionCollisionException
from pyonepassword.api.object_types import OPLoginItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_item_get_login_section_collision_01(signed_in_op: OP):
    """
    Test getting non-conformant item through OP.item_get()

    Verify exception is raised
    """
    # get item "Login Item Section Collisions" --vault "Test Data"
    item_name = "Login Item Section Collisions"
    vault = "Test Data"
    # expected = expected_login_item_data.data_for_login(item_name)
    with pytest.raises(OPSectionCollisionException):
        signed_in_op.item_get(item_name, vault=vault)


def test_item_get_login_section_collision_02(signed_in_op: OP,
                                             expected_login_item_data: ExpectedLoginItemData):
    """
    Test getting non-conformant item through OP.item_get(), using relaxed validation

    Verify:
        - an OPLoginItem is returned as expected
        - the item contains expected values
    """
    # get item "Login Item Section Collisions" --vault "Test Data"
    item_name = "Login Item Section Collisions"
    expected = expected_login_item_data.data_for_login(item_name)
    vault = "Test Data"
    # expected = expected_login_item_data.data_for_login(item_name)
    item = signed_in_op.item_get(
        item_name, vault=vault, relaxed_validation=True)
    assert isinstance(item, OPLoginItem)
    assert item.username == expected.username


def test_item_get_login_section_collision_03(signed_in_op: OP):
    """
    Test getting an non-conformant item's password field through OP.item_get_password()

    Verify an exception is raised
    """
    item_name = "Login Item Section Collisions"
    vault = "Test Data"
    with pytest.raises(OPSectionCollisionException):
        signed_in_op.item_get_password(item_name, vault=vault)


def test_item_get_login_section_collision_04(signed_in_op: OP,
                                             expected_login_item_data: ExpectedLoginItemData):
    """
    Test getting an non-conformant item's password field through OP.item_get_password(), with relaxed validation

    Verify:
        - a password value is returned
        - the password matches the expected value
    """
    item_name = "Login Item Section Collisions"
    expected: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name)
    vault = "Test Data"

    result = signed_in_op.item_get_password(
        item_name, vault=vault, relaxed_validation=True)
    assert result == expected.password
