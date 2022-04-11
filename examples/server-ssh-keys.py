import os
import getpass
from pathlib import Path
from argparse import ArgumentParser
from pyonepassword import OP, OPServerItem, OPNotSignedInException


class ServerWithSSHKeys:
    SSH_KEYS_SECTION = "SSH Keys"
    PRIV_PERMS = 0o600
    PUB_PERMS = 0o644
    DIR_PERMS = 0o755

    def __init__(self, server_item: OPServerItem):
        self._server: OPServerItem = server_item

    def ssh_key_pair(self, identity_name, pub_only):
        identity_name_pub = f"{identity_name}.pub"
        priv_key = None
        if not pub_only:
            priv_key = self._server.field_value_by_section_title(
                "SSH Keys", identity_name)
        pub_key = self._server.field_value_by_section_title(
            "SSH Keys", identity_name_pub)
        return (priv_key, pub_key)

    def write_ssh_keys(self, outdir, identity_name, pub_only=False):
        priv, pub = self.ssh_key_pair(identity_name, pub_only)
        self._mkdir(outdir)
        if not pub_only:
            fpath = Path(outdir, identity_name)
            self._write_with_octal_perms(fpath, self.PRIV_PERMS, priv)
        fpath = Path(outdir, f"{identity_name}.pub")
        self._write_with_octal_perms(fpath, self.PUB_PERMS, pub)

    def _mkdir(self, dirpath):
        dirpath.mkdir(mode=self.DIR_PERMS, parents=True, exist_ok=True)

    def _write_with_octal_perms(self, fpath, octal_perms: int, data):
        if isinstance(data, bytes):
            mode = "wb"
        elif isinstance(data, str):
            mode = "w"
        else:
            raise Exception("Unknown data type for writing")

        with open(os.open(fpath, os.O_CREAT | os.O_WRONLY, octal_perms), mode) as f:
            f.write(data)


def do_signin(vault="Machine Credentials"):
    try:
        op = OP(use_existing_session=True, password_prompt=False)
    except OPNotSignedInException:
        print("Existing session not found")
        my_password = getpass.getpass(prompt="1Password master password:\n")
        op = OP(vault="Test Data", password=my_password)

    return op


def do_parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "server_name", help="Name of server to fetch SSH keys for")
    parser.add_argument("key_name", help="Name of SSH identity file")
    parser.add_argument(
        "--pub-only", help="Only fetch public key for identity", action="store_true")
    parser.add_argument(
        "--outdir", help="Optional directory to write keys to. Default is CWD")
    parser.add_argument(
        "--vault", help="Optional name of 1Password vault to search")

    parsed = parser.parse_args()
    return parsed


def main():
    args = do_parse_args()
    vault = args.vault
    server_name = args.server_name
    key_name = args.key_name

    if vault:
        op = do_signin(vault=vault)
    else:
        op = do_signin()

    if args.outdir:
        outdir = Path(args.outdir)
    else:
        outdir = Path(".")

    server: OPServerItem = op.item_get(server_name)
    server: ServerWithSSHKeys = ServerWithSSHKeys(server)
    server.write_ssh_keys(outdir, key_name, args.pub_only)


if __name__ == "__main__":
    main()
