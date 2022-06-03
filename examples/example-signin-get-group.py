import getpass
import os
import sys

parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import OP, OPVaultGetException  # noqa: E402


def do_signin():
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(prompt="1Password master password:\n")
    # You may optionally provide an account shorthand if you used a custom one during initial sign-in
    # shorthand = "arbitrary_account_shorthand"
    # return OP(account_shorthand=shorthand, password=my_password)
    # Or we'll try to look up account shorthand from your latest sign-in in op's config file
    return OP(password=my_password)


if __name__ == "__main__":

    op = do_signin()

    print("Signed in.")
    print("Looking up vault \"Team Members\"...")
    try:
        group_dict = op.group_get("Team Members")
        print(group_dict)
        print("")
        print("Vaults can also be looked up by their uuid")
        print("")
        print("Looking up uuid \"yhdg6ovhkjcfhn3u25cp2bnl6e\"...")
        group_dict_2 = op.group_get("yhdg6ovhkjcfhn3u25cp2bnl6e")
        print("Vault dictionaries match? {}".format(group_dict == group_dict_2))
    except OPVaultGetException as ope:
        print("1Password lookup failed: {}".format(ope))
        print(ope.err_output)
        exit(ope.returncode)
