import os
import sys

from do_signin import do_signin

parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
# isort: split
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import OPGroup, OPVaultGetException  # noqa: E402

if __name__ == "__main__":

    op = do_signin()

    print("Signed in.")
    print("Looking up vault \"Team Members\"...")
    try:
        group: OPGroup = op.group_get("Team Members")
        print(group)
        print("")
        print("Vaults can also be looked up by their uuid")
        print("")
        print("Looking up uuid \"yhdg6ovhkjcfhn3u25cp2bnl6e\"...")
        group_2: OPGroup = op.group_get("yhdg6ovhkjcfhn3u25cp2bnl6e")
        print("Vault dictionaries match? {}".format(group == group_2))
    except OPVaultGetException as ope:
        print("1Password lookup failed: {}".format(ope))
        print(ope.err_output)
        exit(ope.returncode)
