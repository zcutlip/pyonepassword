#!/usr/bin/env python3

import os
import sys

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


def main():
    version_support = OPVersionSupport()
    min_ver = str(version_support.minimum_version)
    supported_ver = str(version_support.supported_version)
    readme_text = open(README_TEMPLATE, "r").read()
    readme_text = readme_text.replace(MIN_VER_PLACEHOLDER, min_ver)
    readme_text = readme_text.replace(SUPPORTED_VER_PLACEHOLDER, supported_ver)
    with open(README, "w") as f:
        f.write(readme_text)


if __name__ == "__main__":
    exit(main())
