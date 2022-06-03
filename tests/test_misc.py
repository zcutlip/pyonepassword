from __future__ import annotations

import pytest

from pyonepassword import OP
from pyonepassword._op_cli_config import OPCLIConfig

# ensure HOME env variable is set, and there's a valid op config present
# pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_get_account_shorthand_01(signed_in_op: OP):
    op_config = OPCLIConfig()
    shorthand = signed_in_op._get_account_shorthand(op_config)
    assert shorthand == "example_shorthand"


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
def test_get_account_shorthand_02(signed_in_op: OP):
    op_config = OPCLIConfig()
    shorthand = signed_in_op._get_account_shorthand(op_config)
    assert shorthand is None


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_alt_op_env")
def test_uses_bio_property_01():
    op = OP(op_path='mock-op', account_shorthand="example_shorthand")
    assert not op.uses_bio


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_alt_op_env")
def test_session_var_property_01(expected_misc_data):
    expected_var_name = expected_misc_data.data_for_key("op-session-var")
    op = OP(op_path='mock-op', account_shorthand="example_shorthand")
    assert op.session_var == expected_var_name
