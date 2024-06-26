import pytest

from pyonepassword._op_cli_version import (
    OPCLIVersion,
    OPCLIVersionSupportException,
    OPVersionSupport
)

VERSION_STRING_2_26_0 = "2.26.0"
VERSION_STRING_2_26_0_beta_01 = "2.26.0-beta.01"
VERSION_STRING_2_26_0_beta_14 = "2.26.0-beta.14"

VERSION_STRING_2_27_0 = "2.27.0"
VERSION_STRING_2_27_0_beta_12 = "2.27.0-beta.12"
VERSION_STRING_2_27_0_beta_14 = "2.27.0-beta.14"

# leading zeroes in the beta number can break things
VERSION_STRING_2_28_0_beta_01 = "2.28.0-beta.01"


""" ########## Test less-than ########## """


def test_cli_version_lt_010():
    """
    Create OPCLIVersion objects from two different version strings

    Compare the second to the first using less-than

    Verify:
        The first, lower version object is less than the second
    """
    v1 = OPCLIVersion(VERSION_STRING_2_26_0)
    v2 = OPCLIVersion(VERSION_STRING_2_27_0)
    assert v1 < v2


def test_cli_version_lt_020():
    """
    Create an OPCLIVersion object from a beta version string

    Compare a non-beta string of the same major/minor/patch version to the object using less-than

    Verify:
        The version object is less than the non-beta version string
    """
    ver_obj = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    assert ver_obj < VERSION_STRING_2_26_0


def test_cli_version_lt_030():
    """
    Create two OPCLIVersion objects from beta version strings, the first version being a lower minor & beta version than the second.

    Compare the two objects using less-than

    Verify:
        The first, lower version object is less than the second
    """
    beta_ver_1 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_ver_2 = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert beta_ver_1 < beta_ver_2


def test_cli_version_lt_040():
    """
    Create an OPCLIVersion object from a version string

    Assign the version object to a second variable

    Compare the object to itself via the two variables, using less-than

    Verify:
        The object is not less than itself
    """
    v1 = OPCLIVersion(VERSION_STRING_2_26_0)
    v2 = v1

    assert not v1 < v2


def test_cli_version_lt_050():
    """
    Create version objects from a non-beta version string and a beta, but higher version string

    Compare the two objects using less-than

    Verify:
        The non-beta version object is less than the beta object
    """
    ver = OPCLIVersion(VERSION_STRING_2_26_0)
    beta_ver = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert ver < beta_ver


def test_cli_version_lt_060():
    """
    Create version objects from a non-beta version string and a beta version string

    Compare the two objects using less-than

    Verify:
        The beta version object is less than the non-beta version object
    """
    beta_ver = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    ver = OPCLIVersion(VERSION_STRING_2_27_0)
    assert beta_ver < ver


""" ########## Test less-than or equal ########## """


def test_cli_version_le_070():
    """
    Create OPCLIVersion objects from two different version strings

    Compare the second to the first using less-than-or-equal

    Verify:
        The first, lower version object is less than or equal to the second
    """
    ver1 = OPCLIVersion(VERSION_STRING_2_26_0)
    ver2 = OPCLIVersion(VERSION_STRING_2_27_0)
    assert ver1 <= ver2


def test_cli_version_le_080():
    """
    Create an OPCLIVersion object from a beta version string

    Compare a non-beta string of the same major/minor/patch version to the object using less-than-or-equal

    Verify:
        The version object is less than or equal to the non-beta version string
    """
    ver_obj = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    assert ver_obj <= VERSION_STRING_2_26_0


def test_cli_version_le_090():
    """
    Create two OPCLIVersion objects from beta version strings, the first version being a lower minor & beta version than the second.

    Compare the two objects using less-than-or-equal

    Verify:
        The first, lower version object is less than or equal to the second
    """
    beta_ver_1 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_ver_2 = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert beta_ver_1 <= beta_ver_2


def test_cli_version_le_100():
    """
    Create an OPCLIVersion object from a version string

    Assign the version object to a second variable

    Compare the object to itself via the two variables, using less-than-or-equal

    Verify:
        The object is less than or equal to itself
    """
    v1 = OPCLIVersion(VERSION_STRING_2_26_0)
    v2 = v1

    assert v1 <= v2


def test_cli_version_le_110():
    """
    Create version objects from a non-beta version string and a beta, but higher version string

    Compare the two objects using less-than-or-equal

    Verify:
        The non-beta version object is less than or equal to the beta object
    """
    ver = OPCLIVersion(VERSION_STRING_2_26_0)
    beta_ver = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert ver <= beta_ver


def test_cli_version_le_120():
    """
    Create version objects from a non-beta version string and a beta version string

    Compare the two objects using less-than-or-equal

    Verify:
        The beta version object is less than or equal to the non-beta object
    """
    beta_ver = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    ver = OPCLIVersion(VERSION_STRING_2_27_0)
    assert beta_ver <= ver


def test_cli_version_le_130():
    """
    Create a OPCLIVersion object from a version string

    Compare the version object to the version string using less-than-or-equal

    Verify:
        The version object is less than or equal to the strin
    """
    version_obj = OPCLIVersion(VERSION_STRING_2_26_0)
    assert version_obj <= VERSION_STRING_2_26_0


def test_cli_version_le_140():
    """
    Test round-tripping a version string to a version object and back

    Create:
     - a version object from a beta version string
     - a new version string from the beta version object

     Verify:
        The object is less than or equal to the string
    """
    beta_version_obj = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_version_str = str(beta_version_obj)
    print(VERSION_STRING_2_26_0_beta_01)
    print(beta_version_str)
    # these are equal, so <= passes
    assert beta_version_obj <= beta_version_str


""" ########## Test greater-than ########## """


def test_cli_version_gt_160():
    """
    Create OPCLIVersion objects from two different version strings

    Compare the second to the first using less-than

    Verify:
        The second, higher version object is greater than the second
    """
    v1 = OPCLIVersion(VERSION_STRING_2_26_0)
    v2 = OPCLIVersion(VERSION_STRING_2_27_0)
    assert v2 > v1


def test_cli_version_gt_170():
    """
    Create a OPCLIVersion object

    Compare the object to a lower version string using greater-than

    Verify:
        The version object is greater than the lower version string
    """
    ver = OPCLIVersion(VERSION_STRING_2_27_0)
    assert ver > VERSION_STRING_2_26_0


def test_cli_version_gt_180():
    """
    Create an OPCLIVersion object from a beta version string

    Compare the object to a non-beta string of the same major/minor/patch using greater-than

    Verify:
        The object is greater than the lower version string
    """
    ver_obj = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert ver_obj > VERSION_STRING_2_26_0


def test_cli_version_gt_190():
    """
    Test round-tripping a version string to a version object and back

    Create:
     - a version object from a beta version string
     - a new version string from the beta version object

     Verify:
        The object is not greater than the string
    """
    beta_version_obj = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_version_str = str(beta_version_obj)
    print(VERSION_STRING_2_26_0_beta_01)
    print(beta_version_str)
    # these are equal, so '>' is false
    assert not beta_version_obj > beta_version_str


def test_cli_version_gt_200():
    """
    Create two OPCLIVersion objects from beta version strings, the first version being a lower minor & beta version than the second.

    Compare the two objects using greater-than

    Verify:
        The second, higher version object is greater than the second
    """
    beta_ver_1 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_ver_2 = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert beta_ver_2 > beta_ver_1


def test_cli_version_gt_210():
    """
    Create an OPCLIVersion object from a version string

    Assign the version object to a second variable

    Compare the object to itself via the two variables, using greater-than

    Verify:
        The object is not greater than itself
    """
    v1 = OPCLIVersion(VERSION_STRING_2_26_0)
    v2 = v1

    assert not v2 > v1


def test_cli_version_gt_220():
    """
    Create version objects from a non-beta version string and a beta, but higher version string

    Compare the two objects using greater-than

    Verify:
        The beta version object is greater than the lower, non-beta version object
    """
    ver = OPCLIVersion(VERSION_STRING_2_26_0)
    beta_ver = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert beta_ver > ver


def test_cli_version_gt_230():
    """
    Create version objects from a non-beta version string and a beta version string

    Compare the two objects using greater-than

    Verify:
        The non-beta version object is greater than the lower, beta version object
    """
    beta_ver = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    ver = OPCLIVersion(VERSION_STRING_2_27_0)
    assert ver > beta_ver


def test_cli_version_gt_240():
    """
    Create version objects from a non-beta version string and a beta version string

    Compare the two objects using greater-than

    Verify:
        The non-beta version object is greater than the beta version object
    """
    ver = OPCLIVersion(VERSION_STRING_2_26_0)
    beta_ver = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    assert ver > beta_ver


def test_cli_version_gt_250():
    """
    Create two OPCLIVersion objects from beta version strings, the first version being a lower beta version than the second, but the same major/minor/patch.

    Compare the two objects using greater-than

    Verify:
        The second, higher version object is greater than the first
    """
    beta_ver_1 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_ver_2 = OPCLIVersion(VERSION_STRING_2_26_0_beta_14)
    assert beta_ver_2 > beta_ver_1


def test_cli_version_gt_260():
    """
    Create two OPCLIVersion objects from beta version strings, the first version being a lower minor & beta version than the second.

    Compare the two objects using greater-than

    Verify:
        The second, higher version object is greater than the first
    """
    beta_ver_1 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_ver_2 = OPCLIVersion(VERSION_STRING_2_27_0_beta_14)
    assert beta_ver_2 > beta_ver_1


""" ########## Test greater than or equal ########## """


def test_cli_version_ge_270():
    """
    Create OPCLIVersion objects from two different version strings

    Compare the second to the first using greater-than-or-equal

    Verify:
        The second, higher version object is greater than or equal to the second
    """
    v1 = OPCLIVersion(VERSION_STRING_2_26_0)
    v2 = OPCLIVersion(VERSION_STRING_2_27_0)
    assert v2 >= v1


def test_cli_version_ge_280():
    """
    Create an OPCLIVersion object from a version string

    Compare the object to a lower version string

    Verify:
        The version object is greater than or equal to the lower version string
    """
    ver = OPCLIVersion(VERSION_STRING_2_27_0)
    assert ver >= VERSION_STRING_2_26_0


def test_cli_version_ge_290():
    """
    Create an OPCLIVersion object from a beta version string

    Compare a non-beta string of the same major/minor/patch version to the object using greater-than-or-equal

    Verify:
        The object is greater than or equal to the lower version string
    """
    ver_obj = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert ver_obj >= VERSION_STRING_2_26_0


def test_cli_version_ge_300():
    """
    Test round-tripping a version string to a version object and back

    Create:
     - a version object from a beta version string
     - a new version string from the beta version object

     Verify:
        The object is not greater or equal to than the string
    """
    beta_version_obj = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_version_str = str(beta_version_obj)
    print(VERSION_STRING_2_26_0_beta_01)
    print(beta_version_str)
    # these are equal, so '>' is false
    assert beta_version_obj >= beta_version_str


def test_cli_version_ge_310():
    """
    Create two OPCLIVersion objects from beta version strings, the first version being a lower minor & beta version than the second.

    Compare the two objects using greater-than

    Verify:
        The second, higher version object is greater than or equal to the second
    """
    beta_ver_1 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_ver_2 = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert beta_ver_2 >= beta_ver_1


def test_cli_version_ge_320():
    """
    Create an OPCLIVersion object from a version string

    Assign the version object to a second variable

    Compare the object to itself via the two variables, using greater-than-or-equal

    Verify:
        The object is not greater than or equal to itself
    """
    v1 = OPCLIVersion(VERSION_STRING_2_26_0)
    v2 = v1

    assert v2 >= v1


def test_cli_version_ge_330():
    """
    Create version objects from a non-beta version string and a beta, but higher version string

    Compare the two objects using greater-than-or-equal

    Verify:
        The beta version object is greater than or equal to the lower, non-beta version object
    """
    ver = OPCLIVersion(VERSION_STRING_2_26_0)
    beta_ver = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert beta_ver >= ver


def test_cli_version_ge_340():
    """
    Create version objects from a non-beta version string and a beta version string

    Compare the two objects using greater-than-or-equal

    Verify:
        The non-beta version object is greater than or equal to the lower, beta version object
    """
    beta_ver = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    ver = OPCLIVersion(VERSION_STRING_2_27_0)
    assert ver >= beta_ver


def test_cli_version_ge_350():
    """
    Create version objects from a non-beta version string and a beta version string

    Compare the two objects using greater-than

    Verify:
        The non-beta version object is greater than the beta version object
    """
    ver = OPCLIVersion(VERSION_STRING_2_26_0)
    beta_ver = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    assert ver >= beta_ver


def test_cli_version_ge_360():
    """
    Create two OPCLIVersion objects from beta version strings, the first version being a lower beta version than the second, but the same major/minor/patch.

    Compare the two objects using greater-than-or-equal

    Verify:
        The second, higher version object is greater than or equal to the first
    """
    beta_ver_1 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_ver_2 = OPCLIVersion(VERSION_STRING_2_26_0_beta_14)
    assert beta_ver_2 >= beta_ver_1


def test_cli_version_ge_370():
    """
    Create two OPCLIVersion objects from beta version strings, the first version being a lower minor & beta version than the second.

    Compare the two objects using greater-than-or-equal

    Verify:
        The second, higher version object is greater than or equal to the first
    """
    beta_ver_1 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_ver_2 = OPCLIVersion(VERSION_STRING_2_27_0_beta_14)
    assert beta_ver_2 >= beta_ver_1


""" ########## Test equality ########## """


def test_cli_version_eq_250():
    """
    Create a OPCLIVersion object from a version string

    Compare the version object to the version string using equality

    Verify:
        The version object and string are equal
    """
    version_obj = OPCLIVersion(VERSION_STRING_2_26_0)
    assert version_obj == VERSION_STRING_2_26_0


def test_cli_version_eq_260():
    """
    Test round-tripping a version string to a version object and back

    Create:
     - a version object from a beta version string
     - a new version string from the beta version object

     Verify:
        The object and the new string are equal
    """
    beta_version_obj = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_version_str = str(beta_version_obj)
    print(VERSION_STRING_2_26_0_beta_01)
    print(beta_version_str)
    assert beta_version_str == beta_version_obj


def test_cli_version_eq_270():
    """
    Test round-tripping a version string to a version object and back

    Create:
     - a version object from a beta version string
     - a new version string from the beta version object

     Verify:
        The original string and the new string are equal
    """
    beta_version_obj = OPCLIVersion(VERSION_STRING_2_28_0_beta_01)
    beta_version_str = str(beta_version_obj)
    print(VERSION_STRING_2_28_0_beta_01)
    print(beta_version_str)
    assert beta_version_str == VERSION_STRING_2_28_0_beta_01


def test_cli_version_beta_280():
    """
    Test OPCLIVersion.is_beta property

    Create OPCLIVersion object from a non-beta version string

    Verify:
        The object's is_beta property is false
    """
    ver = OPCLIVersion(VERSION_STRING_2_26_0)

    assert ver.is_beta is False


def test_cli_version_check_290(deprecated_version_str):
    """
    Test OPVersionSupport.check_version()'s handling of deprecated version strings

    Call version_support.check_version() on a deprecated version string

    Verify: DeprecationWarning is issued
    """
    version_support = OPVersionSupport()
    print(f"testing deprecated version string: {deprecated_version_str}")

    assert isinstance(deprecated_version_str, str)

    # not useful to inspect the warnings_list produced by warns()
    # it may collect other warnings not relevent to the test
    with pytest.warns(DeprecationWarning):
        version_support.check_version_support(deprecated_version_str)


def test_cli_version_check_300(deprecated_version_obj):
    """
    Test OPVersionSupport.check_version()'s handling of deprecated version objects

    Call version_support.check_version() on a OPCLIVersion object equal to a deprecated version

    Verify: DeprecationWarning is issued
    """
    version_support = OPVersionSupport()
    print(f"testing deprecated version obj: {deprecated_version_obj}")

    assert isinstance(deprecated_version_obj, OPCLIVersion)
    # not useful to inspect the warnings_list produced by warns()
    # it may collect other warnings not relevent to the test
    with pytest.warns(DeprecationWarning):
        version_support.check_version_support(deprecated_version_obj)


def test_cli_version_check_310(unsupported_version_str):
    """
    Test OPVersionSupport.check_version()'s handling of unsupported version strings

    Call version_support.check_version() on an unsupported version string

    Verify: OPCLIVersionSupportException is raised
    """
    version_support = OPVersionSupport()
    print(f"testing unsupported version obj: {unsupported_version_str}")

    assert isinstance(unsupported_version_str, str)

    with pytest.raises(OPCLIVersionSupportException):
        version_support.check_version_support(unsupported_version_str)


def test_cli_version_check_320(unsupported_version_obj):
    """
    Test OPVersionSupport.check_version()'s handling of unsupported objects

    Call version_support.check_version() on a OPCLIVersion object equal to an unsupported version

    Verify: OPCLIVersionSupportException is raised
    """
    version_support = OPVersionSupport()
    print(f"testing unsupported version str: {unsupported_version_obj}")

    assert isinstance(unsupported_version_obj, OPCLIVersion)

    with pytest.raises(OPCLIVersionSupportException):
        version_support.check_version_support(unsupported_version_obj)
