from __future__ import annotations

from typing import TYPE_CHECKING, List

import pytest

from pyonepassword.api.object_types import (
    OPConcealedField,
    OPLoginItem,
    OPStringField,
    OPTOTPField
)
from pyonepassword.op_items.field_registry import OPItemFieldFactory

if TYPE_CHECKING:
    from .fixtures.expected_item_fields import (
        ExpectedItemField,
        ExpectedItemFieldData
    )
    from .fixtures.expected_login import ExpectedLogin
    from .fixtures.valid_data import ValidData


def _lookup_exepcted_item_field(fields: List[ExpectedItemField], field_id: str):
    """
    Field order may not be reliable, so we have to hunt for the right one
    """
    field = None
    for f in fields:
        if f.field_id == field_id:
            field = f
    return field


# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_item_field_01(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")
    field = OPItemFieldFactory.item_field(field_dict)
    assert isinstance(field, OPStringField)
    assert field.field_id == expected.field_id


def test_item_field_02(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")
    field = OPItemFieldFactory.item_field(field_dict)
    assert field.field_type == expected.type


def test_item_field_03(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")
    field = OPItemFieldFactory.item_field(field_dict)
    assert field.reference is not None
    assert field.reference == expected.reference


def test_item_field_04(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")
    field = OPItemFieldFactory.item_field(field_dict)
    assert field.label == expected.label


def test_item_field_05(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")
    field = OPItemFieldFactory.item_field(field_dict)
    assert field.value == expected.value


def test_item_field_06(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-username")
    field_dict = valid_data.data_for_name("login-item-field-username")
    field = OPItemFieldFactory.item_field(field_dict)
    assert field.purpose == expected.purpose


def test_item_field_11(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemFieldFactory.item_field(field_dict)
    assert isinstance(field, OPConcealedField)
    assert field.field_id == expected.field_id


def test_item_field_12(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemFieldFactory.item_field(field_dict)
    assert field.field_type == expected.type


def test_item_field_13(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemFieldFactory.item_field(field_dict)
    assert field.reference is not None
    assert field.reference == expected.reference


def test_item_field_14(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemFieldFactory.item_field(field_dict)
    assert field.label == expected.label


def test_item_field_15(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemFieldFactory.item_field(field_dict)
    assert field.value == expected.value


def test_item_field_16(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemFieldFactory.item_field(field_dict)
    assert field.purpose == expected.purpose


def test_item_field_17(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField
    expected = expected_item_field_data.data_for_key("example-login-password")
    field_dict = valid_data.data_for_name("login-item-field-password")
    field = OPItemFieldFactory.item_field(field_dict)
    assert isinstance(field.entropy, float)
    margin = .000001
    expected_entropy = expected.entropy
    high = expected_entropy * (1 + margin)
    low = expected_entropy * (1 - margin)
    assert field.entropy < high
    assert field.entropy > low


def test_item_field_18(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key(
        "example-totp-field-no-issuer")
    field_dict = valid_data.data_for_name("login-item-field-totp")
    field: OPTOTPField = OPItemFieldFactory.item_field(field_dict)
    assert isinstance(field, OPTOTPField)
    assert field.totp == expected.totp


def test_item_field_19(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    expected: ExpectedItemField

    expected = expected_item_field_data.data_for_key(
        "example-totp-field-no-issuer")
    field_dict = valid_data.data_for_name("login-item-field-totp")
    field: OPTOTPField = OPItemFieldFactory.item_field(field_dict)
    assert isinstance(field, OPTOTPField)
    assert field.totp_secret == expected.value


def test_item_lookup_field_01(valid_data: ValidData, expected_login_item_data):
    item_name = "Example Login with Fields"
    field_label = "Example Field"
    field_id = "zyhpoqkrwjtrq6qh5vhwylh6ie"
    expected_login: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name)

    expected_field_list: ExpectedItemField = expected_login.fields_by_label(
        field_label)
    expected_field = _lookup_exepcted_item_field(expected_field_list, field_id)

    valid_item_dict = valid_data.data_for_name("example-login-with-fields")
    result_login_item = OPLoginItem(valid_item_dict)
    result = result_login_item.fields_by_label(field_label)
    result = result[1]
    assert result.value == expected_field.value


def test_item_lookup_field_02(valid_data: ValidData, expected_login_item_data):
    item_name = "Example Login with Fields"
    field_label = "Example Field"
    field_id = "ikr76mnggw767qwqoel624oqv4"
    expected_login: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name)

    expected_field_list: ExpectedItemField = expected_login.fields_by_label(
        field_label)
    expected_field = _lookup_exepcted_item_field(expected_field_list, field_id)

    valid_item_dict = valid_data.data_for_name("example-login-with-fields")
    result_login_item = OPLoginItem(valid_item_dict)
    result = result_login_item.first_field_by_label(field_label)

    assert result.value == expected_field.value


def test_item_lookup_field_03(valid_data: ValidData, expected_login_item_data):
    """
    Test case-insensitive field lookup by label

    Create:
        - a login item with fields and sections
        - case-insensitively look up a field via first_field_by_label()
    Verify:
        - the lookup succeeded
        - the resulting field matches the expected value
    """
    item_name = "Example Login with Fields"
    field_label = "Example Field"
    field_id = "ikr76mnggw767qwqoel624oqv4"
    expected_login: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name)

    expected_field_list: ExpectedItemField = expected_login.fields_by_label(
        field_label)
    expected_field = _lookup_exepcted_item_field(expected_field_list, field_id)

    valid_item_dict = valid_data.data_for_name("example-login-with-fields")
    result_login_item = OPLoginItem(valid_item_dict)
    field_label_lower = field_label.lower()
    result = result_login_item.first_field_by_label(
        field_label_lower, case_sensitive=False)

    assert result.value == expected_field.value
