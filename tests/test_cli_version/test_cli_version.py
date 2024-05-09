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
    v1 = OPCLIVersion(VERSION_STRING_2_26_0)
    v2 = OPCLIVersion(VERSION_STRING_2_27_0)
    assert v1 < v2


def test_cli_version_lt_020():
    ver_obj = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    assert ver_obj < VERSION_STRING_2_26_0


def test_cli_version_lt_030():
    beta_ver_1 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_ver_2 = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert beta_ver_1 < beta_ver_2


def test_cli_version_lt_040():
    v1 = OPCLIVersion(VERSION_STRING_2_26_0)
    v2 = v1

    assert not v1 < v2


def test_cli_version_lt_050():
    ver = OPCLIVersion(VERSION_STRING_2_26_0)
    beta_ver = OPCLIVersion(VERSION_STRING_2_27_0_beta_12)
    assert ver < beta_ver


def test_cli_version_lt_060():
    beta_ver = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    ver = OPCLIVersion(VERSION_STRING_2_27_0)
    assert beta_ver < ver


""" ########## Test less-than or equal ########## """


def test_cli_version_le_070():
    ver1 = OPCLIVersion(VERSION_STRING_2_26_0)
    ver2 = OPCLIVersion(VERSION_STRING_2_27_0)
    assert ver1 <= ver2


""" ########## Test greater-than ########## """


def test_cli_version_gt_080():
    ver = OPCLIVersion(VERSION_STRING_2_26_0)
    beta_ver = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    assert ver > beta_ver


def test_cli_version_gt_090():
    beta_ver_1 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_ver_2 = OPCLIVersion(VERSION_STRING_2_26_0_beta_14)
    assert beta_ver_2 > beta_ver_1


def test_cli_version_gt_100():
    beta_ver_1 = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_ver_2 = OPCLIVersion(VERSION_STRING_2_27_0_beta_14)
    assert beta_ver_2 > beta_ver_1


""" ########## Test equality ########## """


def test_cli_version_eq_110():
    version_obj = OPCLIVersion(VERSION_STRING_2_26_0)
    assert version_obj == VERSION_STRING_2_26_0


def test_cli_version_eq_120():
    beta_version_obj = OPCLIVersion(VERSION_STRING_2_26_0_beta_01)
    beta_version_str = str(beta_version_obj)
    print(VERSION_STRING_2_26_0_beta_01)
    print(beta_version_str)
    assert beta_version_str == beta_version_obj


def test_cli_version_eq_130():
    beta_version_obj = OPCLIVersion(VERSION_STRING_2_28_0_beta_01)
    beta_version_str = str(beta_version_obj)
    print(VERSION_STRING_2_28_0_beta_01)
    print(beta_version_str)
    assert beta_version_str == VERSION_STRING_2_28_0_beta_01


def test_cli_version_beta_140():
    ver = OPCLIVersion(VERSION_STRING_2_26_0)

    assert ver.is_beta is False


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
