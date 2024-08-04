#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser

# isort: split
parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.insert(0, parent_path)

from pyonepassword._op_cli_version import OPVersionSupport  # noqa: E402

MIN_VER_PLACEHOLDER = "MINIMUM_CLI_VERSION__"
SUPPORTED_VER_PLACEHOLDER = "SUPPORTED_CLI_VERSION__"
README_TEMPLATE = "_readme_template.md"
README = "README.md"


def generate_readme_text(template_path):
    version_support = OPVersionSupport()
    min_ver = str(version_support.minimum_version)
    supported_ver = str(version_support.supported_version)
    readme_text = open(README_TEMPLATE, "r").read()
    readme_text = readme_text.replace(MIN_VER_PLACEHOLDER, min_ver)
    readme_text = readme_text.replace(SUPPORTED_VER_PLACEHOLDER, supported_ver)
    return readme_text


def check_readme(readme_path, readme_text):
    old_readme_text = open(readme_path, "r").read()
    needs_update = old_readme_text != readme_text
    return needs_update


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--check", "-c", help="Check readme only, do not update", action="store_true")
    args = parser.parse_args()
    readme_text = generate_readme_text(README_TEMPLATE)
    needs_update = check_readme(README, readme_text)
    if args.check:
        print("README needs updating")
        return int(needs_update)

    if needs_update:
        with open(README, "w") as f:
            f.write(readme_text)
        print("README updated")


if __name__ == "__main__":
    exit(main())
