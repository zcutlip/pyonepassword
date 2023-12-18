from __future__ import annotations

from typing import TYPE_CHECKING

from pyonepassword.api.exceptions import OPUserGetException

if TYPE_CHECKING:
    from pyonepassword import OP


import pytest

pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("setup_stateful_user_edit_new_user_name")
def test_user_edit_set_name_010(signed_in_team_account_op: OP):
    """
    Test: OP.user_edit()
        - retrieve a user based on username
        - set new username for a user
        - retrieve the user based on the new username
        - set the old username back for the same user
        - retrieve the user based on the original username
    Verify:
        - the original user object's user ID matches the expected user ID
        - the updated user object's user ID matches the expected user ID
        - the restored user object's user ID matches the expected user ID
    """

    user_name = "Example User"
    new_user_name = "Example User (new)"
    expected_user_id = "IT52W465L3IOUUUCSD3WBNL26M"

    existing_user = signed_in_team_account_op.user_get(user_name)
    user_id = existing_user.unique_id
    assert user_id == expected_user_id

    signed_in_team_account_op.user_edit(user_id, new_name=new_user_name)

    updated_user = signed_in_team_account_op.user_get(new_user_name)

    assert updated_user.unique_id == expected_user_id

    signed_in_team_account_op.user_edit(user_id, new_name=user_name)

    updated_user = signed_in_team_account_op.user_get(user_name)

    assert updated_user.unique_id == expected_user_id


@pytest.mark.usefixtures("setup_stateful_user_edit_new_user_name")
def test_user_edit_set_name_020(signed_in_team_account_op: OP):
    """
    Test: OP.user_edit()
        - retrieve a user based on username
        - set new username for a user
        - Attempt to retrieve the user based on the original username
    Verify:
        - the original user object's user ID matches the expected user ID
        - OPUserGetException is raised
    """

    original_user_name = "Example User"
    new_user_name = "Example User (new)"
    expected_user_id = "IT52W465L3IOUUUCSD3WBNL26M"

    existing_user = signed_in_team_account_op.user_get(original_user_name)
    user_id = existing_user.unique_id
    assert user_id == expected_user_id

    signed_in_team_account_op.user_edit(user_id, new_name=new_user_name)

    with pytest.raises(OPUserGetException):
        signed_in_team_account_op.user_get(original_user_name)
