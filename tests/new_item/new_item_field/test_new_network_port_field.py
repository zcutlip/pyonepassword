# __future__.annotations, and typing.TYPE_CHECKING
# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from typing import TYPE_CHECKING

from pyonepassword.op_items.fields_sections._new_fields import (
    OPNewNetworkPortField
)

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    # non-runtime imports here
    from ...fixtures.expected_item_fields import (
        ExpectedItemField,
        ExpectedItemFieldData
    )
    from ...fixtures.valid_data import ValidData


def _assert_valid_numerical_string(number):
    assert isinstance(number, str)
    converted = int(number, 0)
    assert converted >= 0


def test_new_network_port_field_01(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    """
    Create a new OPNewNetworkPortField from a numerical port string
    Verify the 'value' property:
        - is a string
        - is a valid representation of a numeric value >= 0
        - equals the input port string
    """
    field_dict = valid_data.data_for_name("login-item-field-network-port-str")

    expected: ExpectedItemField = expected_item_field_data.data_for_key(
        "example-network-port-field-1")
    expected_port_num = expected.value

    field_id = field_dict["id"]
    new_field = OPNewNetworkPortField(
        field_id, field_dict["value"], field_id=field_id)
    _assert_valid_numerical_string(expected_port_num)
    _assert_valid_numerical_string(new_field.value)
    assert new_field.value == expected_port_num


def test_new_network_port_field_02(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    """
    Create a new OPNewNetworkPortField from an integer
    Verify the 'value' property:
        - is a string
        - is a valid representation of a numeric value >= 0
        - is equivalent to the input port string
    """

    field_dict = valid_data.data_for_name("login-item-field-network-port-int")

    expected: ExpectedItemField = expected_item_field_data.data_for_key(
        "example-network-port-field-2")
    expected_port_num = expected.value

    input_port_num = field_dict["value"]
    assert isinstance(input_port_num, int)
    field_id = field_dict["id"]

    new_field = OPNewNetworkPortField(
        field_id, input_port_num, field_id=field_id)

    _assert_valid_numerical_string(expected_port_num)
    _assert_valid_numerical_string(new_field.value)

    # new field value should not be equal to input value
    # since input value gets converted to a string
    assert new_field.value != input_port_num
    assert new_field.value == expected_port_num


def test_new_network_port_field_03(valid_data: ValidData, expected_item_field_data: ExpectedItemFieldData):
    """
    Create a new OPNewNetworkPortField from an integer
    Verify the 'value' property:
        - is a string
        - is a valid representation of a numeric value >= 0
        - is equivalent to the input port string
    """

    field_dict = valid_data.data_for_name(
        "login-item-field-network-port-str-hex")

    expected: ExpectedItemField = expected_item_field_data.data_for_key(
        "example-network-port-field-3")
    expected_port_num = expected.value

    input_port_num = field_dict["value"]

    _assert_valid_numerical_string(input_port_num)
    assert input_port_num.startswith("0x")

    field_id = field_dict["id"]

    new_field = OPNewNetworkPortField(
        field_id, input_port_num, field_id=field_id)

    _assert_valid_numerical_string(expected_port_num)
    _assert_valid_numerical_string(new_field.value)

    assert new_field.value == expected_port_num
