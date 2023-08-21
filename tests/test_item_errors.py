from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.exceptions import (
    OPFieldNotFoundException,
    OPInvalidItemException,
    OPItemFieldCollisionException,
    OPSectionCollisionException,
    OPSectionNotFoundException,
    OPUnknownItemTypeException
)
from pyonepassword.api.object_types import OPLoginItem
from pyonepassword.op_items import OPItemFactory

if TYPE_CHECKING:
    from .fixtures.invalid_data import InvalidData
    from .fixtures.valid_data import ValidData


# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_unknown_item_type_01(invalid_data):
    """
    Attempt to create an op item with invalid category "UNKNOWN"

    Verify OPUnknownItemtypeException is raised
    """
    invalid_item_json = invalid_data.data_for_name("invalid-item")
    with pytest.raises(OPUnknownItemTypeException):
        _ = OPItemFactory.op_item(invalid_item_json)


def test_malformed_item_json_01(invalid_data):
    """
    Attempt to create an op item with malformed/corrupted JSON

    Verify OPInvalidItemException is raised
    """
    malformed_json = invalid_data.data_for_name("malformed-item-json")
    with pytest.raises(OPInvalidItemException):
        _ = OPItemFactory.op_item(malformed_json)


def test_item_field_not_found_01(valid_data: ValidData):
    """
    Create:
        - a valid OPLoginItem object

    Attempt to look up a non-existent field via field_by_id()

    Verify OPFieldNotFoundException is raised
    """
    item_dict = valid_data.data_for_name("example-login-1")
    result = OPLoginItem(item_dict)

    with pytest.raises(OPFieldNotFoundException):
        result.field_by_id("Non-existent-field")


def test_item_field_not_found_02(valid_data: ValidData):
    """
    Create:
        - a valid OPLoginItem object

    Attempt to look up a non-existent field via fields_by_label()

    Verify OPFieldNotFoundException is raised
    """
    item_dict = valid_data.data_for_name("example-login-1")
    result = OPLoginItem(item_dict)

    with pytest.raises(OPFieldNotFoundException):
        result.fields_by_label("Non-existent-field")


def test_item_field_not_found_03(valid_data: ValidData):
    """
    Create:
        - a valid OPLoginItem object

    Attempt to look up a non-existent field via first_field_by_label()

    Verify OPFieldNotFoundException is raised
    """
    item_dict = valid_data.data_for_name("example-login-1")
    result = OPLoginItem(item_dict)

    with pytest.raises(OPFieldNotFoundException):
        result.first_field_by_label("Non-existent-field")


def test_item_field_collision_01(invalid_data):
    """
    Test item creation with colliding sections

    Create:
        - op item object from an item dictionary with colliding Field IDs
    Verify:
        - OPFieldCollisionException is raised
    """
    field_collision_json = invalid_data.data_for_name("field-collision")
    with pytest.raises(OPItemFieldCollisionException):
        OPItemFactory.op_item(field_collision_json)


def test_item_section_collision_01(invalid_data: InvalidData):
    """
    Test item creation with colliding sections

    Create:
        - op item object from an item dictionary with colliding sections
    Verify:
        - OPSectionCollisionException is raised
    """
    invalid_item_dict = invalid_data.data_for_name(
        "login-item-with-section-collision")
    with pytest.raises(OPSectionCollisionException):
        OPItemFactory.op_item(invalid_item_dict)


def test_item_section_not_found_01(valid_data: ValidData):
    """
    Test looking up a section on a login item by an invalid section ID

    Create:
        - A login item object with fields and sections
        - Look up an invalid section ID via section_by_id()
    Verify:
        - OPSectionNotFoundException is raised
    """
    section_id = "no_such_section"

    valid_item_dict = valid_data.data_for_name("example-login-with-fields")
    result_login_item = OPLoginItem(valid_item_dict)

    with pytest.raises(OPSectionNotFoundException):
        result_login_item.section_by_id(section_id)


def test_item_section_not_found_02(valid_data: ValidData):
    """
    Test looking up a section on a login item by an invalid section ID

    Create:
        - A login item object with fields and sections
        - Look up an invalid section ID via section_by_id()
    Verify:
        - OPSectionNotFoundException is raised
    """
    section_label = "No Such Section"

    valid_item_dict = valid_data.data_for_name("example-login-with-fields")
    result_login_item = OPLoginItem(valid_item_dict)

    with pytest.raises(OPSectionNotFoundException):
        result_login_item.sections_by_label(section_label)


def test_item_section_not_found_03(valid_data: ValidData):
    """
    Test looking up a section on a login item by an invalid section ID

    Create:
        - A login item object with fields and sections
        - Look up an invalid section ID via section_by_id()
    Verify:
        - OPSectionNotFoundException is raised
    """
    section_label = "No Such Section"

    valid_item_dict = valid_data.data_for_name("example-login-with-fields")
    result_login_item = OPLoginItem(valid_item_dict)

    with pytest.raises(OPSectionNotFoundException):
        result_login_item.first_section_by_label(section_label)
