#!/usr/bin/env python3
import sys
from argparse import ArgumentParser

from tests.fixtures.expected_data import ExpectedData
from tests.fixtures.expected_item import ExpectedItemData
from tests.fixtures.expected_item_list import ExpectedItemListData
from tests.fixtures.invalid_data import InvalidData
from tests.fixtures.valid_data import ValidData

known_registries = {
    "valid-data": ValidData,
    "invalid-data": InvalidData,
    "expected-data": ExpectedData,
    "expected-item-list-data": ExpectedItemListData,
    "expected-item-data": ExpectedItemData
}


def sort_registry(registry_name):
    registry_class = known_registries[registry_name]
    registry = registry_class()
    registry.sort_registry_to_disk()


def parse_args():
    parser = ArgumentParser()
    registry_names = ", ".join(list(known_registries.keys()))
    parser.add_argument(
        "registry_name", help=f"Name of the registry to sort. Registry names include: {registry_names}")

    parsed = parser.parse_args()
    return parsed


def main():
    options = parse_args()
    try:
        print(f"sorting registry: {options.registry_name}")
        sort_registry(options.registry_name)
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        return -1


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        exit(127)
