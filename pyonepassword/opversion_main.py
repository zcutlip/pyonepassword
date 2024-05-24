import os
import sys
from argparse import ArgumentParser

from ._op_cli_version import OPVersionSupport


def opversion_parse_args():
    parser = ArgumentParser()
    parser.add_argument("-m",
                        "--minimum-version",
                        action="store_true",
                        help="Print the minimum supported 'op' CLI version")
    parser.add_argument("-s",
                        "--supported-version",
                        action="store_true",
                        help="Print the supported 'op' CLI version threshold")
    parser.add_argument(
        "--raw", help="Write output suitable for piping to another process", action='store_true')

    parsed = parser.parse_args()
    return parsed


def write_output(version, raw: bool):
    version_str = str(version)
    if raw:
        if os.isatty(sys.stdout.fileno()):
            version_str = f"{version_str}\n"
        sys.stdout.write(version_str)
        sys.stdout.flush()
    else:
        print(f"Minimum version: {version_str}")


def main():
    args = opversion_parse_args()
    raw: bool = args.raw
    version_support = OPVersionSupport()
    if args.minimum_version:
        write_output(version_support.minimum_version, raw)

    if args.supported_version:
        write_output(version_support.supported_version, raw)
