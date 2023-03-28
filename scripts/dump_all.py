import json
from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path
from typing import Optional

from do_signin import do_signin

from pyonepassword import OP
from pyonepassword.api.exceptions import OPItemGetException
from pyonepassword.op_items.fields_sections.item_section import (
    OPItemFieldCollisionException,
    OPSectionCollisionException
)
# HACK: I need to export this but haven't yet, so we're using non-API
from pyonepassword.op_items.item_types._item_base import (
    OPAbstractItemDescriptor
)
# HACK: more non-API usage
from pyonepassword.op_objects import OPVaultDescriptor


def dump_all_parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("path", help="Path to dump 1Password items to")
    parser.add_argument("--log", metavar="LOG_PATH",
                        help="Enable logging to the specified log path")
    parser.add_argument("--relaxed-validation",
                        help="Enable the 'relaxed_validation' flag when instantiating item objects", action="store_true")
    parser.add_argument("--include-archive",
                        help="Retrieve items from the archive as well",
                        action="store_true")

    parsed = parser.parse_args()
    return parsed


def log(log_path: Optional[Path], message: str):
    if log_path:
        with open(log_path, "a") as f:
            f.write(f"{message}\n")


def create_log_path(log_path: Optional[Path]):
    if log_path:
        log_path = Path(log_path)
        parent = log_path.parent
        parent.mkdir(parents=True, exist_ok=True)

    start_msg = f"\nStarted: {datetime.now()}\n-----------------"
    log(log_path, start_msg)


def handle_item_error(item: OPAbstractItemDescriptor,
                      error_dir: Path,
                      log_path: Path,
                      exception: Exception):
    error_path = Path(error_dir, "error.txt")
    if error_path.exists():
        log(log_path, "    -> error.txt exists")
    else:
        log(log_path, "    -> error")

        error_dir.mkdir(parents=True, exist_ok=True)
        lines = [
            f"{exception}",
            f"item: {item.title} [{item.unique_id}]",
            f"created: {item.created_at}",
            f"updated: {item.updated_at}"]
        error_text = "\n".join(lines)
        print(error_text)
        print("------")
        print("")

        with open(error_path, "w") as f:
            f.write(error_text)


def process_item(op: OP,
                 item: OPAbstractItemDescriptor,
                 log_path: Path,
                 vault_path: Path,
                 archive: bool = False,
                 relaxed_validation: bool = False):
    log(log_path, f"Item: {item.unique_id}")
    json_path = Path(vault_path, f"{item.unique_id}.json")
    error_dir = Path(
        vault_path, f"{item.unique_id}")
    if not json_path.exists():
        try:
            item = op.item_get(item.unique_id,
                               include_archive=archive,
                               relaxed_validation=relaxed_validation,
                               generic_okay=True)
        except (OPItemFieldCollisionException, OPSectionCollisionException) as e:
            handle_item_error(item, error_dir, log_path, e)
        else:
            with open(json_path, "w") as fp:
                json.dump(item, fp, indent=2)
            log(log_path, "    -> success")


def process_vault(op: OP, vault: OPVaultDescriptor, options: Namespace):
    log_path = options.log
    archive = options.include_archive
    dump_path = Path(options.path)

    print(f"Dumping vault {vault.name}")
    log(log_path, f"Vault: {vault.name}")

    vault_id = vault.unique_id
    vault_path = Path(dump_path, vault_id)
    vault_path.mkdir(parents=True, exist_ok=True, mode=0o700)

    item_list = op.item_list(
        vault=vault.unique_id, include_archive=archive)

    for item_descriptor in item_list:
        process_item(op,
                     item_descriptor,
                     log_path,
                     vault_path,
                     archive=archive,
                     relaxed_validation=options.relaxed_validation)


def main():
    options = dump_all_parse_args()
    print(f"relaxed validation: {options.relaxed_validation}")
    log_path = options.log
    create_log_path(log_path)
    dump_path = Path(options.path)
    dump_path.mkdir(parents=True, exist_ok=True, mode=0o700)
    op: OP = do_signin()
    vault_list = op.vault_list()

    for vault in vault_list:
        try:

            process_vault(op, vault, options)
        except OPItemGetException as e:
            print("Item get failed:")
            print(f"{e.err_output}")
            return e.returncode


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(130)
