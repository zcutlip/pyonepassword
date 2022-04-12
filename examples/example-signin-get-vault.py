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

from pyonepassword import OPGetVaultException  # noqa: E402


if __name__ == "__main__":

    op = do_signin()

    print("Signed in.")
    print("Looking up vault \"Test Data\"...")
    try:
        vault_dict = op.get_vault("Test Data")
        print(vault_dict)
        print("")
        print("Vaults can also be looked up by their uuid")
        print("")
        print("Looking up uuid \"yhdg6ovhkjcfhn3u25cp2bnl6e\"...")
        vault_dict_2 = op.get_vault("yhdg6ovhkjcfhn3u25cp2bnl6e")
        print("Vault dictionaries match? {}".format(vault_dict == vault_dict_2))
    except OPGetVaultException as ope:
        print("1Password lookup failed: {}".format(ope))
        print(ope.err_output)
        exit(ope.returncode)
