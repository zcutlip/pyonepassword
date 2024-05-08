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


def test_cli_version_010():
    v200 = OPCLIVersion(VERSION_STRING_2_26_0)
    v210 = OPCLIVersion(VERSION_STRING_2_27_0)
    assert v200 < v210


def test_cli_version_020():
    v200 = OPCLIVersion(VERSION_STRING_2_26_0)

    assert v200.is_beta is False


def test_cli_version_030():
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    assert v200_beta12 < VERSION_STRING_2_26_0


def test_cli_version_040():
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    v210_beta12 = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert v200_beta12 < v210_beta12


def test_cli_version_050():
    v200_a = OPCLIVersion(VERSION_STRING_2_26_0)
    v200_b = v200_a

    assert not v200_a < v200_b


def test_cli_version_060():
    v210 = OPCLIVersion(VERSION_STRING_2_27_0)
    v210_beta12 = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert v210_beta12 < v210


def test_cli_version_070():
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    v210 = OPCLIVersion(VERSION_STRING_2_27_0)
    assert v200_beta12 < v210


""" ########## Test less-than or equal ########## """


def test_cli_version_080():
    v200 = OPCLIVersion(VERSION_STRING_2_26_0)
    v210 = OPCLIVersion(VERSION_STRING_2_27_0)
    assert v200 <= v210


""" ########## Test greater-than ########## """


def test_cli_version_090():
    v200 = OPCLIVersion(VERSION_STRING_2_26_0)
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    assert v200 > v200_beta12


def test_cli_version_100():
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    v200_beta14 = OPCLIVersion(VERSION_STRING_2_26_0_beta_14)
    assert v200_beta14 > v200_beta12


def test_cli_version_110():
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    v200_beta14 = OPCLIVersion(VERSION_STRING_2_26_0_beta_14)
    assert v200_beta14 > v200_beta12


""" ########## Test equality ########## """


def test_cli_version_120():
    v200 = OPCLIVersion(VERSION_STRING_2_26_0)
    assert v200 == VERSION_STRING_2_26_0


def test_cli_version_130():
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    v200_beta12_str = str(v200_beta12)
    print(VERSION_STRING_2_26_0_beta_01)
    print(v200_beta12_str)
    assert v200_beta12_str == VERSION_STRING_2_26_0_beta_01


def test_cli_version_140():
    v2_18_0_beta_01 = OPCLIVersion(VERSION_STRING_2_28_0_beta_01)
    v2_18_0_beta_01_str = str(v2_18_0_beta_01)
    print(VERSION_STRING_2_28_0_beta_01)
    print(v2_18_0_beta_01_str)
    assert v2_18_0_beta_01_str == VERSION_STRING_2_28_0_beta_01


def test_cli_version_check_150(deprecated_version_str):
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


def test_cli_version_check_160(deprecated_version_obj):
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


def test_cli_version_check_170(unsupported_version_str):
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


def test_cli_version_check_180(unsupported_version_obj):
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
