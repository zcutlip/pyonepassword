from __future__ import annotations

from typing import TYPE_CHECKING

from pyonepassword.api.exceptions import OPUserEditException

if TYPE_CHECKING:
    from pyonepassword import OP


import pytest

pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("setup_stateful_user_edit_travel_mode")
def test_user_edit_travel_mode_010(signed_in_team_account_op: OP):
    """
    Test: OP.user_edit()
        - set travel mode on for a user
        - set travel mode off for the same user
    Verify:
        - No exception is raised for either operation
        - The user name is correctly converted to the expected user ID for both edit operations

    """
    # There isn't, as of this writing, any way to verify travel mode has been turned
    # on or off
    # nothing about travel mode shows up in `op user get`,
    # and for reasons that aren't clear, travel mode restrictions only affect the apps,
    # not `op item get/list` or `op vault list`, so it's not possible to check if a user
    # has/does not have access to something when travel mode is enabled
    #
    # so there isn't really much to test here other than:
    # - we're constructing the CLI arguments correctly
    # - mock-op has a corresponding response to those CLI args
    # - nothing blew up when the response generator ran `op` with those args
    # - user name gets converted to expected user ID
    user_name = "Example User"
    expected_user_id = "IT52W465L3IOUUUCSD3WBNL26M"

    edited_user_id = signed_in_team_account_op.user_edit(
        user_name, travel_mode=True)
    assert edited_user_id == expected_user_id

    edited_user_id = signed_in_team_account_op.user_edit(
        user_name, travel_mode=False)
    assert edited_user_id == expected_user_id


@pytest.mark.usefixtures("setup_stateful_user_edit_travel_mode")
def test_user_edit_travel_mode_020(signed_in_team_account_op: OP):
    """
    Test: OP.user_edit()
        - Edit a user, providing a user name for a non-existent user
    Verify:
        - OPUserEditException is raised
    """
    user_id = "no-such-user"
    with pytest.raises(OPUserEditException):
        signed_in_team_account_op.user_edit(user_id, travel_mode=True)


@pytest.mark.usefixtures("setup_stateful_user_edit_travel_mode")
def test_user_edit_travel_mode_030(signed_in_team_account_op: OP):
    """
    Test: OP.user_edit()
        - Edit a user, providing a user ID for a non-existent user
    Verify:
        - OPUserEditException is raised
    """
    invalid_user_id = "TQ2EKE3TPSK4YDFRMLRVG54Y4U"
    with pytest.raises(OPUserEditException):
        signed_in_team_account_op.user_edit(invalid_user_id, travel_mode=True)
