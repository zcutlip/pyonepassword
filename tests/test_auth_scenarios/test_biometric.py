"""
Test various authentication specifically related to
biometric being enabled/not enabled
"""
from __future__ import annotations

import pytest

from pyonepassword import OP
from pyonepassword.api.exceptions import OPAuthenticationException


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_alt_op_env")
def test_uses_bio_property_01():
    """
    simulate an pyonepassword environment that doesn't use biometric auth
    check that op.uses_bio is False
    """
    op = OP(op_path='mock-op', account="example_shorthand")
    assert not op._uses_bio


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
@pytest.mark.usefixtures("setup_normal_op_env")
def test_uses_biometric_class_method_01(console_logger):
    """
    Test calling OP.uses_biometric() as a class method
    """

    assert OP.uses_biometric(op_path="mock-op")


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
@pytest.mark.usefixtures("setup_no_bio_alt_op_env")
def test_no_bio_no_account_01(console_logger):
    """
    test the conditions:
      - biometric is not enabled
      - no account identifier provided during sign-in
      - no "latest_signin" to infer account identifier from
    """

    OP(op_path='mock-op', password="made-up-password", logger=console_logger)


@pytest.mark.usefixtures("valid_op_cli_config_no_shorthand")
@pytest.mark.usefixtures("setup_no_bio_alt_op_env")
def test_no_bio_no_account_02(console_logger):
    """
    test the conditions:
      - biometric is not enabled
      - no password provided
    """
    with pytest.raises(OPAuthenticationException):
        OP(op_path='mock-op', password_prompt=False, logger=console_logger)
