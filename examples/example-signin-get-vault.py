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

from pyonepassword.api.exceptions import OPVaultGetException  # noqa: E402
from pyonepassword.api.object_types import OPVault  # noqa: E402

if __name__ == "__main__":

    op = do_signin()

    print("Signed in.")
    print("Looking up vault \"Test Data\"...")
    try:
        vault_1: OPVault = op.vault_get("Test Data")
        pprint(vault_1, sort_dicts=False, indent=2)
        print("")
        print("Vaults can also be looked up by their uuid")
        print("")
        print("Looking up uuid \"yhdg6ovhkjcfhn3u25cp2bnl6e\"...")
        vault_2: OPVault = op.vault_get("yhdg6ovhkjcfhn3u25cp2bnl6e")

        print("Vault dictionaries match? {}".format(vault_1.unique_id == vault_2.unique_id and
                                                    vault_1.name == vault_2.name and
                                                    vault_1.description == vault_2.description and
                                                    vault_1.item_count == vault_2.item_count and
                                                    vault_1.created_at == vault_2.created_at and
                                                    vault_1.updated_at == vault_2.updated_at))
    except OPVaultGetException as ope:
        print("1Password lookup failed: {}".format(ope))
        print(ope.err_output)
        exit(ope.returncode)
