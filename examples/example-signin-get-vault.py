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

from pyonepassword import OPVault, OPGetVaultException  # noqa: E402


if __name__ == "__main__":

    op = do_signin()

    print("Signed in.")
    print("Looking up vault \"Test Data\"...")
    try:
        vault_1: OPVault = op.get_vault("Test Data")
        print(vault_1)
        print("")
        print("Vaults can also be looked up by their uuid")
        print("")
        print("Looking up uuid \"yhdg6ovhkjcfhn3u25cp2bnl6e\"...")
        vault_2: OPVault = op.get_vault("yhdg6ovhkjcfhn3u25cp2bnl6e")
        if (vault_1.unique_id == vault_2.unique_id and
                vault_1.name == vault_2.name):
            pass
        print("Vault dictionaries match? {}".format(vault_1.unique_id == vault_2.unique_id and
                                                    vault_1.name == vault_2.name and
                                                    vault_1.description == vault_2.description and
                                                    vault_1.items == vault_2.items and
                                                    vault_1.created_at == vault_2.created_at and
                                                    vault_1.updated_at == vault_2.updated_at))
    except OPGetVaultException as ope:
        print("1Password lookup failed: {}".format(ope))
        print(ope.err_output)
        exit(ope.returncode)
