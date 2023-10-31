from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from pyonepassword.api.object_types import OPLoginItem

if TYPE_CHECKING:
    from .fixtures.valid_data import ValidData
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
#     Check that OP(use_existing_session=True) produces deprecation warnings
#     """
#     with warnings.catch_warnings(record=True) as warning_list:
#         OP(op_path='mock-op', use_existing_session=True, password_prompt=False)
#         assert warning_list
#         print(f"warning_list: {len(warning_list)}")


def test_deprecated_method_01(valid_data: ValidData, expected_login_item_data):
    """
    OPAbstractItem.field_value_by_section_title() has been replaced with
    field_value_by_section_label()

    Verify a deprecation warning is generated
    """
    field_label = "Example Field"
    section_label = "Example Section 1"

    valid_item_dict = valid_data.data_for_name("example-login-with-fields")
    result_login_item = OPLoginItem(valid_item_dict)

    with warnings.catch_warnings(record=True) as warnings_list:
        result_login_item.field_value_by_section_title(
            section_label, field_label)
        assert len(warnings_list) > 0
