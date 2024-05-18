import pytest

from pyonepassword import OP
from pyonepassword._op_cli_version import OPCLIVersion
from pyonepassword.api.exceptions import OPConfigNotFoundException
from pyonepassword.py_op_exceptions import OPWhoAmiException


@pytest.mark.usefixtures("invalid_op_cli_config_missing")
@pytest.mark.usefixtures("setup_no_conf_no_bio_env")
def test_missing_op_config_010(console_logger):

    with pytest.raises(OPConfigNotFoundException):
        OP(op_path="mock-op", logger=console_logger)


@pytest.mark.usefixtures("invalid_op_cli_config_missing")
@pytest.mark.usefixtures("setup_no_conf_no_bio_env")
def test_missing_op_config_020(console_logger):
    """
    Simulate:
    - running op --format json account list with no ~/.config/op/
    - Integration with the desktop app, and hence biometric, is disabled

    Verify:
        an empty list is returned
    """
    OP.set_logger(console_logger)
    accounts = OP._get_account_list(op_path="mock-op")
    assert len(accounts) == 0


@pytest.mark.usefixtures("invalid_op_cli_config_missing")
@pytest.mark.usefixtures("setup_no_conf_no_bio_env")
def test_missing_op_config_030(console_logger):
    """
    Simulate:
    - running op --format json whoami with no ~/.config/op/
    - Integration with the desktop app, and hence biometric, is disabled

    Verify:
        OPWhoAmiException is raised
    """
    OP.set_logger(console_logger)
    with pytest.raises(OPWhoAmiException):
        OP._whoami(op_path="mock-op")


@pytest.mark.usefixtures("invalid_op_cli_config_missing")
@pytest.mark.usefixtures("setup_no_conf_no_bio_env")
def test_missing_op_config_040(console_logger):
    """
    Simulate:
    - running op --version with no ~/.config/op/
    - Integration with the desktop app, and hence biometric, is disabled

    Verify:
        a version is returned
        version is instance of OPCLIVersion
    """
    OP.set_logger(console_logger)
    version = OP._get_cli_version(op_path="mock-op")
    assert version
    assert isinstance(version, OPCLIVersion)


@pytest.mark.usefixtures("invalid_op_cli_config_missing")
@pytest.mark.usefixtures("setup_no_conf_no_bio_env")
def test_missing_op_config_050(console_logger):
    """
    Simulate:
    - running op --format json whoami <account_uuid> with no ~/.config/op/
    - Integration with the desktop app, and hence biometric, is disabled

    Verify:
        OPWhoAmiException is raised
    """
    account_uuid = "5GHHPJK5HZC5BAT7WDUXW57G44"
    OP.set_logger(console_logger)
    with pytest.raises(OPWhoAmiException):
        OP._whoami(op_path="mock-op", account=account_uuid)
