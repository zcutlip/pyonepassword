import pathlib
import shutil

import pytest

from pyonepassword import OP
from pyonepassword._op_cli_version import OPCLIVersionSupportException
from pyonepassword.api.exceptions import OPNotFoundException


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("deprecated_version_op_env")
def test_op_class_deprecated_version_010(console_logger):
    """
    Test OP initialization with a deprecated CLI version

    Verify: DeprecationWarning is issued
    """
    # not useful to inspect the warnings_list produced by warns()
    # it may collect other warnings not relevent to the test
    with pytest.warns(DeprecationWarning):
        OP(op_path="mock-op", logger=console_logger)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("deprecated_version_op_env")
def test_op_class_deprecated_version_020(console_logger):
    """
    Test calling an OP class method with a deprecated CLI version

    Verify: DeprecationWarning is issued
    """
    OP.set_logger(console_logger)
    with pytest.warns(DeprecationWarning):
        OP._whoami("mock-op")


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("unsupported_version_op_env")
def test_op_class_unsupported_version_030(console_logger):
    """
    Test OP initialization with an unsupported CLI version

    Verify: OPCLIVersionSupportException is raised
    """
    with pytest.raises(OPCLIVersionSupportException):
        OP(op_path="mock-op", logger=console_logger)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("unsupported_version_op_env")
def test_op_class_unsupported_version_040(console_logger):
    """
    Test calling an OP class method with an unsupported CLI version

    Verify: OPCLIVersionSupportException is raised
    """
    OP.set_logger(console_logger)
    with pytest.raises(OPCLIVersionSupportException):
        OP._whoami("mock-op")


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("deprecated_version_op_env")
def test_op_public_version_check_deprecated_050(console_logger):
    """
    Test public OP.check_op_version() method with a deprecated CLI version string

    Verify: DeprecationWarning is issued
    """
    # not useful to inspect the warnings_list produced by warns()
    # it may collect other warnings not relevent to the test
    OP.set_logger(console_logger)
    with pytest.warns(DeprecationWarning):
        OP.check_op_version("mock-op")


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("unsupported_version_op_env")
def test_op_public_version_check_unsupported_060(console_logger):
    """
    Test public OP.check_op_version() method with an unsupported CLI version string

    Verify: OPCLIVersionSupportException is raised
    """
    OP.set_logger(console_logger)
    with pytest.raises(OPCLIVersionSupportException):
        OP.check_op_version("mock-op")


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("unsupported_version_op_env")
def test_op_public_version_check_unsupported_070(console_logger):
    """
    Test public OP.check_op_version() method with an unsupported CLI version string,
    passing a pathlib.Path object rather than op_path as a string

    Verify: OPCLIVersionSupportException is raised
    """
    op_path = pathlib.Path(shutil.which("mock-op"))
    OP.set_logger(console_logger)
    with pytest.raises(OPCLIVersionSupportException):
        OP.check_op_version(op_path)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("unsupported_version_op_env")
def test_op_public_version_check_invalid_op_path_080(console_logger):
    """
    Test public OP.check_op_version() method with an invalid path to the op command

    Verify: OPNotFoundException is raised
    """
    op_path = "no-such-op"
    OP.set_logger(console_logger)
    with pytest.raises(OPNotFoundException):
        OP.check_op_version(op_path)
