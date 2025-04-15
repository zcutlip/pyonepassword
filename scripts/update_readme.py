#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser
from collections.abc import Iterable

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


DO_NOT_EDIT_COMMENT_LINES = [
    "Managed by 'scripts/update_readme.py'. Do not edit.",
    f"Changes should be made to {README_TEMPLATE}"]


def generate_comment_header(comment_lines):
    """
    This should produce something like:

    [//]: # (-------------------------------------------------)
    [//]: # (This may be the most platform independent comment)
    [//]: # (-------------------------------------------------)

    """
    # https://stackoverflow.com/a/20885980
    if not isinstance(comment_lines, Iterable):
        raise Exception("comment_lines must be iterable")
    longest = 0
    for line in comment_lines:
        _len = len(line)
        if _len > longest:
            longest = _len
    comment_dashes = f"[//]: # ({'':->{longest}})"
    blank_line = ""
    header_lines = [blank_line,
                    comment_dashes]

    for line in comment_lines:
        comment = f"[//]: # ({line:<{longest}})"
        header_lines.append(comment)

    header_lines.extend([comment_dashes,
                         blank_line,
                         blank_line])

    return header_lines


def generate_readme_text(template_path):
    version_support = OPVersionSupport()
    min_ver = str(version_support.minimum_version)
    supported_ver = str(version_support.supported_version)
    readme_text = open(template_path, "r").read()
    readme_text = readme_text.replace(MIN_VER_PLACEHOLDER, min_ver)
    readme_text = readme_text.replace(SUPPORTED_VER_PLACEHOLDER, supported_ver)
    header_lines = generate_comment_header(DO_NOT_EDIT_COMMENT_LINES)
    header_text = "\n".join(header_lines)
    readme_text = header_text + readme_text
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
        if needs_update:
            print("README needs updating")
        return int(needs_update)

    if needs_update:
        with open(README, "w") as f:
            f.write(readme_text)
        print("README updated")


if __name__ == "__main__":
    exit(main())
