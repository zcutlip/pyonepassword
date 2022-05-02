from pyonepassword.op_cli_version import OPCLIVersion

VERSION_STRING_2_0_0 = "2.0.0"
VERSION_STRING_2_0_0_beta_12 = "2.0.0-beta.12"
VERSION_STRING_2_0_0_beta_14 = "2.0.0-beta.14"

VERSION_STRING_2_1_0 = "2.1.0"
VERSION_STRING_2_1_0_beta_12 = "2.1.0-beta.12"
VERSION_STRING_2_1_0_beta_14 = "2.1.0-beta.14"


def test_cli_version_01():
    v200 = OPCLIVersion(VERSION_STRING_2_0_0)
    v210 = OPCLIVersion(VERSION_STRING_2_1_0)
    assert v200 < v210


def test_cli_version_02():
    v200 = OPCLIVersion(VERSION_STRING_2_0_0)

    assert v200.is_beta is False


def test_cli_version_03():
    v200 = OPCLIVersion(VERSION_STRING_2_0_0)
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_0_0_beta_12)
    assert v200 > v200_beta12


def test_cli_version_04():
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_0_0_beta_12)
    assert v200_beta12 < VERSION_STRING_2_0_0


def test_cli_version_05():
    v200 = OPCLIVersion(VERSION_STRING_2_0_0)
    assert v200 == VERSION_STRING_2_0_0


def test_cli_version_06():
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_0_0_beta_12)
    v200_beta12_str = str(v200_beta12)
    assert v200_beta12_str == VERSION_STRING_2_0_0_beta_12


def test_cli_version_07():
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_0_0_beta_12)
    v210_beta12 = OPCLIVersion(VERSION_STRING_2_1_0_beta_12)
    assert v200_beta12 < v210_beta12


def test_cli_version_08():
    v200_a = OPCLIVersion(VERSION_STRING_2_0_0)
    v200_b = v200_a

    assert not v200_a < v200_b


def test_cli_version_09():
    v200 = OPCLIVersion(VERSION_STRING_2_0_0)
    v210 = OPCLIVersion(VERSION_STRING_2_1_0)
    assert v200 <= v210


def test_cli_version_10():
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_0_0_beta_12)
    v200_beta14 = OPCLIVersion(VERSION_STRING_2_0_0_beta_14)
    assert v200_beta14 > v200_beta12


def test_cli_version_11():
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_0_0_beta_12)
    v200_beta14 = OPCLIVersion(VERSION_STRING_2_0_0_beta_14)
    assert v200_beta14 > v200_beta12


def test_cli_version_12():
    v200_beta12 = OPCLIVersion(VERSION_STRING_2_0_0_beta_12)
    v210 = OPCLIVersion(VERSION_STRING_2_1_0)
    assert v200_beta12 < v210


def test_cli_version_13():
    v210 = OPCLIVersion(VERSION_STRING_2_1_0)
    v210_beta12 = OPCLIVersion(VERSION_STRING_2_1_0_beta_12)
    assert v210_beta12 < v210
