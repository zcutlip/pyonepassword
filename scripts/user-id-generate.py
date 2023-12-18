#!/usr/bin/env python3

from pyonepassword.op_items.uuid import OPUniqueIdentifierBase32


def new_user_id():
    uuid = OPUniqueIdentifierBase32(uppercase=True)
    print(uuid)


if __name__ == "__main__":
    exit(new_user_id())
