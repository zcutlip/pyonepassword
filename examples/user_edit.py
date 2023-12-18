from do_signin import do_signin

from pyonepassword.api.exceptions import OPUserEditException


def user_edit_set_travel_mode():
    op = do_signin()
    user_name = "Example User"

    # Toggle travel mode on
    # user_edit() returns the unique user ID
    user_id = op.user_edit(user_name, travel_mode=True)

    # Toggle travel mode back off
    # When editing users, either user name or unique user ID is okay
    op.user_edit(user_id, travel_mode=False)


def user_edit_set_user_name():
    op = do_signin()
    user_name = "Example User"

    new_user_name = "Example User - updated"

    # set new username
    op.user_edit(user_name, new_user_name=new_user_name)


def user_edit_invalid_user():

    op = do_signin()
    user_name = "Nonexistent User"

    try:
        op.user_edit(user_name, travel_mode=False)
    except OPUserEditException as e:
        print(e.err_output)
