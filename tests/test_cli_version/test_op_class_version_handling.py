import pytest

from pyonepassword import OP


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("deprecated_version_op_env")
def test_op_class_deprecated_version_010(console_logger):
    # not useful to inspect the warnings_list produced by warns()
    # it may collect other warnings not relevent to the test
    with pytest.warns(DeprecationWarning):
        OP(op_path="mock-op", logger=console_logger)


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("deprecated_version_op_env")
def test_op_class_deprecated_version_020(console_logger):
    OP.set_logger(console_logger)
    with pytest.warns(DeprecationWarning):
        OP._whoami("mock-op")
