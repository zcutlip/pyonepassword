#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from typing import List, Optional

import dotenv

from pyonepassword import OP, logging
from pyonepassword.api.constants import LETTERS_DIGITS_SYMBOLS_20
from pyonepassword.api.object_types import (
    OPItemField,
    OPLoginItemTemplate,
    OPNewPasswordField,
    OPPasswordItem,
    OPSection
)
from pyonepassword.op_items.item_types.login import OPNewItemMixin


class OPPasswordItemTemplate(OPNewItemMixin, OPPasswordItem):

    # required for password generation
    PASSWORDS_SUPPORTED = True
    FIELD_ID_PASSWORD = "password"

    def __init__(self,
                 title: str,
                 password: Optional[str] = None,
                 fields: List[OPItemField] = [],
                 sections: List[OPSection] = [],
                 tags: List[str] = []):
        password_field = OPNewPasswordField(
            self.FIELD_ID_PASSWORD,
            password,
            field_id=self.FIELD_ID_PASSWORD
        )
        if fields is None:
            fields = list()
        else:
            fields = list(fields)

        fields.append(password_field)
        super().__init__(title,
                         fields=fields,
                         sections=sections,
                         tags=tags)


def batch_create_parse_args():
    parser = ArgumentParser()
    parser.add_argument("count", help="Number of items to create", type=int)
    parser.add_argument("vault", help="Vault to create login items in")
    parser.add_argument("--name", help="Item base name",
                        default="Example Login Item")
    parser.add_argument("--username", help="Base username", default="user_")
    parser.add_argument(
        "--alternating-tags", help="Comma-separated list of tags to alternate between when creating items")
    parser.add_argument(
        "--url", help="URL string to associate with the items created")
    parser.add_argument(
        "--starting-number", help="Starting number of the first item to create", type=int, default=0)
    parser.add_argument("--category", help="Category of item to create")
    parser.add_argument("--env-file", help="Path to a .env file to load")
    parsed = parser.parse_args()
    return parsed


def create_items(options: Namespace):
    # 1password will prompt for auth, either biometric or on the console
    logger = logging.console_logger("batch_create", level=logging.DEBUG)
    op = OP(logger=logger)
    count = options.count
    vault = options.vault
    item_name_base = options.name
    username_base = options.username
    url = options.url
    start = options.starting_number
    if start < 0:
        raise Exception("Starting number must be >= 0")

    category = "login"
    if options.category:
        category = options.category
    tags = []
    if options.alternating_tags:
        tag_string = options.alternating_tags
        tags = [tag.strip() for tag in tag_string.split(",")]

    print(f"creating {count} {category} items in {vault} vault")
    for i in range(0, count):
        item_num = i + start
        _tags = []
        if tags:
            tagnum = i % len(tags)
            _tags = tags[tagnum:tagnum + 1]
        title = f"{item_name_base} {item_num:02d}"
        password = LETTERS_DIGITS_SYMBOLS_20
        if category == "login":
            username = f"{username_base}{item_num:02d}"
            item_template = OPLoginItemTemplate(
                title, username, url=url, tags=_tags)
        elif category == "password":
            item_template = OPPasswordItemTemplate(title, tags=_tags)
        else:
            raise Exception(f"Unknown category: {category}")
        op.item_create(item_template, password_recipe=password, vault=vault)
    print("done")


def main():
    options = batch_create_parse_args()
    if options.env_file:
        loaded = dotenv.load_dotenv(options.env_file)
        if not loaded:
            print(f"Failed to load env file {options.env_file}")
            return -1
    create_items(options)
    return 0


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("Interruped. terminating")
        exit(130)
