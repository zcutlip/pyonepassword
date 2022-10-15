from __future__ import annotations

from typing import TYPE_CHECKING, List

import pytest

from pyonepassword.api.exceptions import OPSectionNotFoundException
from pyonepassword.api.object_types import OPLoginItem
from pyonepassword.op_items.item_section import OPItemField

if TYPE_CHECKING:
    from .fixtures.expected_item_fields import (
        ExpectedItemField,
        ExpectedItemFieldData
    )
    from .fixtures.expected_login import ExpectedLogin
    from .fixtures.valid_data import ValidData


# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _lookup_exepcted_item_field(fields: List[ExpectedItemField], field_id: str) -> ExpectedItemField:
    """
    Field order may not be reliable, so we have to hunt for the right one
    """
    field = None
    for f in fields:
        if f.field_id == field_id:
            field = f
    return field


def test_item_section_01(valid_data: ValidData, expected_login_item_data: ExpectedItemFieldData):
    """
    Test search for first field by label

    Create:
      - Look up a section on the item object by its ID
      - Look up a field on the seciton object using first_field_by_id()
    Verify:
      - the lookup doesn't fail
      - the returned section's value matches the expected value
    """
    item_name = "Example Login with Fields"
    section_id = "vh4wk7qyw46urc7wuwczzhpm7u"
    field_label = "Example Field"
    field_id = "ikr76mnggw767qwqoel624oqv4"
    expected_login: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name)

    expected_field_list: ExpectedItemField = expected_login.fields_by_label(
        field_label)
    expected_field = _lookup_exepcted_item_field(expected_field_list, field_id)
    valid_item_dict = valid_data.data_for_name("example-login-with-fields")
    result_login_item = OPLoginItem(valid_item_dict)

    result_item_section = result_login_item.section_by_id(section_id)

    result = result_item_section.first_field_by_label(field_label)

    assert isinstance(result, OPItemField)
    assert result.value == expected_field.value


def test_item_section_02(valid_data: ValidData, expected_login_item_data: ExpectedItemFieldData):
    """
    Test case-insensitive search for first field by label

    Create:
      - A login item object with fields and sections
      - Look up a section on the item object by its ID
      - Case-insensitive look up a field on the section object using first_field_by_id()
    Verify:
      - the lookup doesn't fail
      - the returned field

    """
    item_name = "Example Login with Fields"
    section_id = "vh4wk7qyw46urc7wuwczzhpm7u"
    field_label = "EXAMPLE FIELD"
    field_id = "ikr76mnggw767qwqoel624oqv4"
    expected_login: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name)

    expected_field_list: ExpectedItemField = expected_login.fields_by_label(
        field_label)
    expected_field = _lookup_exepcted_item_field(expected_field_list, field_id)
    valid_item_dict = valid_data.data_for_name("example-login-with-fields")
    result_login_item = OPLoginItem(valid_item_dict)

    result_item_section = result_login_item.section_by_id(section_id)

    result = result_item_section.first_field_by_label(
        field_label, case_sensitive=False)

    assert isinstance(result, OPItemField)
    assert result.value == expected_field.value


def test_item_section_03(valid_data: ValidData, expected_login_item_data: ExpectedItemFieldData):
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
