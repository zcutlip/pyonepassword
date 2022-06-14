import os
import sys
from pprint import pprint

from do_signin import do_signin

parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
# isort: split
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import OPUser, OPUserGetException  # noqa: E402

if __name__ == "__main__":

    op = do_signin()

    print("Signed in.")
    print("Looking up user \"Firstname Lastname\"...")
    try:
        user: OPUser = op.user_get("Firstname Lastname")
        pprint(user, sort_dicts=False, indent=2)
        print("")
        print("Users can also be looked up by their uuid")
        print("")
        print("Looking up uuid \"QBXCWKNZZNGL8I3KSZOH5ERLHI\"...")
        user_2: OPUser = op.user_get("QBXCWKNZZNGL8I3KSZOH5ERLHI")
        print("User dictionaries match? {}".format(user == user_2))
    except OPUserGetException as ope:
        print("1Password lookup failed: {}".format(ope))
        print(ope.err_output)
        exit(ope.returncode)
