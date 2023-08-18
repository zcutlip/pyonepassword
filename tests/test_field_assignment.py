from pyonepassword._field_assignment import (
    FieldTypeEnum,
    OPFieldAssignmentPassword,
    _OPFieldAssignment
)


def test_field_type_010():
    """
    Create a field assignment string using:
        - a section label
        - a field label
        - field type "password"
    Verify:
        the resulting field assignment string matches the expected string
    """
    expected_assignment_str = "Section 010.Field 010[password]=Password 010"

    section_label = "Section 010"
    field_label = "Field 010"
    value = "Password 010"
    field_type = FieldTypeEnum.PASSWORD

    assignment = _OPFieldAssignment(
        field_label, value, field_type, section_label=section_label)

    assert expected_assignment_str == assignment


def test_field_type_020():
    """
    Create a field assignment string using:
        - a section label
        - a field label
        - field type "text"
    Verify:
        the resulting field assignment string matches the expected string
    """
    expected_assignment_str = "Section 020.Field 020[text]=text string 020"

    section_label = "Section 020"
    field_label = "Field 020"
    value = "text string 020"
    field_type = FieldTypeEnum.TEXT

    assignment = _OPFieldAssignment(
        field_label, value, field_type, section_label=section_label)

    assert expected_assignment_str == assignment


def test_field_type_030():
    """
    Create a field assignment string using:
        - a section label
        - a field label
        - field type "url"
    Verify:
        the resulting field assignment string matches the expected string
    """
    expected_assignment_str = "Section 030.Field 030[url]=https://fake-url/etc.etc.etc."

    section_label = "Section 030"
    field_label = "Field 030"
    value = "https://fake-url/etc.etc.etc."
    field_type = FieldTypeEnum.URL

    assignment = _OPFieldAssignment(
        field_label, value, field_type, section_label=section_label)

    assert expected_assignment_str == assignment


def test_field_type_password_040():
    """
    Create a field assignment string using:
        - a section label
        - a field label
        - PasswordFieldAssignment class
    Verify:
        the resulting field assignment string matches the expected string
    """
    expected_assignment_str = "Section 040.Field 040[password]=Password 040"

    section_label = "Section 040"
    field_label = "Field 040"
    value = "Password 040"

    assignment = OPFieldAssignmentPassword(
        field_label, value, section_label=section_label)

    assert expected_assignment_str == assignment


def test_field_type_password_050():
    """
    Create a field assignment string using:
        - No section label
        - a field label
        - PasswordFieldAssignment class
    Verify:
        the resulting field assignment string matches the expected string
    """
    expected_assignment_str = "Field 050[password]=Password 050"

    field_label = "Field 050"
    value = "Password 050"

    assignment = OPFieldAssignmentPassword(field_label, value)

    assert expected_assignment_str == assignment


def test_field_assignment_escape_100():
    """
    Create a field assignment string using:
        - a section label containing '=' characters
        - a field label
        - a password containing '=' characters
        - PasswordFieldAssignment class
    Verify:
        - The resulting field assignment contains properly escaped '=' characters in the section label
        - The '=' characters in the password are not escaped

    Note: Part of the purpose of this test case is to exercise character escaping in section labels
        separately from character escaping in field labels
    """
    section_label = "Section=With=Equals"
    field_label = "Field 100"
    value = "Password=With=Equals 100"

    expected_escaped_string = r"Section\=With\=Equals.Field 100[password]=Password=With=Equals 100"
    assignment = OPFieldAssignmentPassword(
        field_label, value, section_label=section_label)

    assert expected_escaped_string == assignment


def test_field_assignment_escape_110():
    """
    Create a field assignment string using:
        - a section label
        - a field label containting '=' characters
        - a password containing '=' characters
        - PasswordFieldAssignment class
    Verify:
        - The resulting field assignment contains properly escaped '=' characters in the field label
        - The '=' characters in the password are not escaped
    Note: Part of the purpose of this test case is to exercise character escaping in field labels
        separately from character escaping in section labels
    """
    section_label = "Section 110"
    field_label = "Field=With=Equals 110"
    value = "Password=With=Equals 110"

    expected_escaped_string = r"Section 110.Field\=With\=Equals 110[password]=Password=With=Equals 110"
    assignment = OPFieldAssignmentPassword(
        field_label, value, section_label=section_label)

    assert expected_escaped_string == assignment


def test_field_assignment_escape_120():
    """
    Create a field assignment string using:
        - a section label containing '.' characters
        - a field label containting '.' characters
        - PasswordFieldAssignment class
    Verify:
        - The resulting field assignment contains properly escaped '.' characters in the
          field and section labels
    """
    section_label = "Section.With.Periods 120"
    field_label = "Field.With.Periods 120"
    value = "Password 120"

    expected_escaped_string = r"Section\.With\.Periods 120.Field\.With\.Periods 120[password]=Password 120"

    assignment = OPFieldAssignmentPassword(
        field_label, value, section_label=section_label)

    assert expected_escaped_string == assignment


def test_field_assignment_escape_130():
    """
    Create a field assignment string using:
        - a section label containing backslash characters
        - a field label containting backslash characters
        - PasswordFieldAssignment class
    Verify:
        - The resulting field assignment contains properly escaped '.' characters in the
          field and section labels
    """
    section_label = r"Section\With\Backslashes 120"
    field_label = r"Field\With\Backslashes 120"

    value = "Password 120"

    expected_escaped_string = r"Section\\With\\Backslashes 120.Field\\With\\Backslashes 120[password]=Password 120"

    assignment = OPFieldAssignmentPassword(
        field_label, value, section_label=section_label)

    assert expected_escaped_string == assignment


def test_field_type_password_redaction_140():
    """
    Create a field assignment string using:
        - A section label
        - A field label
        - PasswordFieldAssignment class
    Verify:
        A string copy of the resulting field assignment appropriately redacts the password
    """
    # this is intentially an equals emoji
    # to prevent the redacted string from
    # accidentally being used as an assignment -------------v
    expected_redacted_str = "Section 140.Field 140[password]🟰************"

    section_label = "Section 140"
    field_label = "Field 140"
    value = "Password 140"

    assignment = OPFieldAssignmentPassword(
        field_label, value, section_label=section_label)

    assert expected_redacted_str == str(assignment)
