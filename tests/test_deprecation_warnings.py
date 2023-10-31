# import warnings

# import pytest


# disabled but left as example
# def example_test_import_deprecation_01():
#     """
#     Import deprecated OPNotSignedInException class from
#     pyonepassword.api.exceptions

#     Ensure there is a deprecation warning
#     """
#     with warnings.catch_warnings(record=True) as warning_list:
#         from pyonepassword.api.exceptions import \
#             OPNotSignedInException  # noqa: F401
#         assert warning_list

# disabled but left as example
# @pytest.mark.usefixtures("valid_op_cli_config_homedir")
# @pytest.mark.usefixtures("setup_op_sess_var_alt_env")
# def example_test_kwarg_deprecation_01():
#     """
#     Simulate a pyonepassword environment that:
#     - doesn't use biometric
#     - DOES have OP_SESSION_<user uuid> env variable set
#     Check that OP(use_existing_session=True) succeeds
#     """
#     with warnings.catch_warnings(record=True) as warning_list:
#         OP(op_path='mock-op', use_existing_session=True, password_prompt=False)
#         assert warning_list
