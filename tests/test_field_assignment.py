from pyonepassword._field_assignment import FieldTypeEnum, _FieldAssignment


def test_field_type_010():
    expected_assignment_str = "Section 010.Field 010[password]=Password 010"

    section_label = "Section 010"
    field_label = "Field 010"
    value = "Password 010"
    field_type = FieldTypeEnum.PASSWORD

    assignment = _FieldAssignment(
        field_label, value, field_type, section_label=section_label)

    assert expected_assignment_str == assignment


def test_field_type_020():
    expected_assignment_str = "Section 020.Field 020[text]=text string 020"

    section_label = "Section 020"
    field_label = "Field 020"
    value = "text string 020"
    field_type = FieldTypeEnum.TEXT

    assignment = _FieldAssignment(
        field_label, value, field_type, section_label=section_label)

    assert expected_assignment_str == assignment


# def test_field_assignment_escape_01():
#     section_label = "Section=With=Equals"
#     field_label = "Field 01"
#     value = "New Password"
#     field_type = FieldTypeEnum.PASSWORD
