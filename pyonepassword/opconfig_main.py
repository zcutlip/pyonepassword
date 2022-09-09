import sys
from argparse import ArgumentParser

from ._op_cli_config import (
    OPCLIAccountConfig,
    OPCLIConfig,
    OPConfigNotFoundException
)


def opc_parse_args():
    parser = ArgumentParser()
    parser.add_argument("--print-account-key",
                        help="Print just the account key instead of the whole config", action='store_true')
    parser.add_argument("--config-path", help="Path to 'op' configuration")
    parser.add_argument("--shorthand", help="Account shorthand to look up")
    parser.add_argument(
        "--raw", help="Write output suitable for piping to another process", action='store_true')

    parsed = parser.parse_args()
    return parsed


def print_config(acct_conf: OPCLIAccountConfig):
    print(f"shorthand: {acct_conf.shorthand}")
    print(f"URL: {acct_conf.url}")
    print(f"email: {acct_conf.email}")
    print(f"Account key: {acct_conf['accountKey']}")
    print(f"Account ID: {acct_conf.account_uuid}")
    print(f"User ID: {acct_conf.user_uuid}")


def main():
    options = opc_parse_args()
    config_path = options.config_path
    shorthand = options.shorthand
    try:
        config = OPCLIConfig(configpath=config_path)
        acct_conf = config.get_config(account_id=shorthand)
    except OPConfigNotFoundException as e:
        print(f"Unable to look up op config: {e}", file=sys.stderr)
        exit(1)

    if not options.raw:
        print(f"Config path: {config.configpath}")
    if options.print_account_key:
        if options.raw:
            sys.stdout.write(acct_conf["accountKey"])
            sys.stdout.flush()
        else:
            print(f"Account key: {acct_conf['accountKey']}")
    else:
        print_config(acct_conf)
