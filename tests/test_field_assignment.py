from pyonepassword._field_assignment import (
    FieldTypeEnum,
    PasswordFieldAssignment,
    _FieldAssignment
)


def test_field_type_010():
    """
    Create a field assignment string using:
        - a section name
        - a field name
        - field type "password"
    Verify:
        the resulting field assignment string matches the expected string
    """
    expected_assignment_str = "Section 010.Field 010[password]=Password 010"

    section_label = "Section 010"
    field_label = "Field 010"
    value = "Password 010"
    field_type = FieldTypeEnum.PASSWORD

    assignment = _FieldAssignment(
        field_label, value, field_type, section_label=section_label)

    assert expected_assignment_str == assignment


def test_field_type_020():
    """
    Create a field assignment string using:
        - a section name
        - a field name
        - field type "text"
    Verify:
        the resulting field assignment string matches the expected string
    """
    expected_assignment_str = "Section 020.Field 020[text]=text string 020"

    section_label = "Section 020"
    field_label = "Field 020"
    value = "text string 020"
    field_type = FieldTypeEnum.TEXT

    assignment = _FieldAssignment(
        field_label, value, field_type, section_label=section_label)

    assert expected_assignment_str == assignment


def test_field_type_030():
    """
    Create a field assignment string using:
        - a section name
        - a field name
        - field type "url"
    Verify:
        the resulting field assignment string matches the expected string
    """
    expected_assignment_str = "Section 030.Field 030[url]=https://fake-url/etc.etc.etc."

    section_label = "Section 030"
    field_label = "Field 030"
    value = "https://fake-url/etc.etc.etc."
    field_type = FieldTypeEnum.URL

    assignment = _FieldAssignment(
        field_label, value, field_type, section_label=section_label)

    assert expected_assignment_str == assignment


def test_field_type_password_040():
    """
    Create a field assignment string using:
        - a section name
        - a field name
        - PasswordFieldAssignment class
    Verify:
        the resulting field assignment string matches the expected string
    """
    expected_assignment_str = "Section 040.Field 040[password]=Password 040"

    section_label = "Section 040"
    field_label = "Field 040"
    value = "Password 040"

    assignment = PasswordFieldAssignment(
        field_label, value, section_label=section_label)

    assert expected_assignment_str == assignment

#     field_type = FieldTypeEnum.PASSWORD
