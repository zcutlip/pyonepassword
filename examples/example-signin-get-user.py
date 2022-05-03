import os
import sys
from do_signin import do_signin
parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import OPGetUserException  # noqa: E402


if __name__ == "__main__":

    op = do_signin()

    print("Signed in.")
    print("Looking up user \"Firstname Lastname\"...")
    try:
        user_dict = op.user_get("Firstname Lastname")
        print(user_dict)
        print("")
        print("Users can also be looked up by their uuid")
        print("")
        print("Looking up uuid \"QBXCWKNZZNGL8I3KSZOH5ERLHI\"...")
        user_dict_2 = op.user_get("QBXCWKNZZNGL8I3KSZOH5ERLHI")
        print("User dictionaries match? {}".format(user_dict == user_dict_2))
    except OPGetUserException as ope:
        print("1Password lookup failed: {}".format(ope))
        print(ope.err_output)
        exit(ope.returncode)
