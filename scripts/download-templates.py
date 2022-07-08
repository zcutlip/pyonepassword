#!/usr/bin/env python3

import json
import os
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import List

# isort: split
parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if parent_path not in sys.path:
    sys.path.append(parent_path)

from examples.do_signin import do_signin  # noqa: E402
from pyonepassword import OP  # noqa: E402
from pyonepassword._op_cli_argv import _OPArgv  # noqa: E402
from pyonepassword.api.exceptions import OPSigninException  # noqa: E402
from pyonepassword.json import safe_unjson  # noqa: E402


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "template_dir", help="Path to write item templates to")
    parser.add_argument("--account", "-A",
                        help="1Password account to use. (See op signin --help, for valid identifiers")
    parsed = parser.parse_args()
    return parsed


class OPItemTemplateDescriptor(dict):
    def __init__(self, template_descriptor_dict: dict):
        super().__init__(template_descriptor_dict)

    @property
    def template_id(self) -> int:
        uuid = self["uuid"]
        template_id = int(uuid)
        return template_id

    @property
    def name(self) -> str:
        return self["name"]

    @property
    def normalized_name(self) -> str:
        name = self.name.lower()
        name = name.replace(' ', '_')
        return name


class OPItemTemplateDescriptorList(List[OPItemTemplateDescriptor]):
    def __init__(self, template_list_or_json):
        super().__init__()
        template_list = safe_unjson(template_list_or_json)
        from pprint import pprint
        pprint(template_list, sort_dicts=False, indent=2)
        for templ_dict in template_list:
            templ_descrip = OPItemTemplateDescriptor(templ_dict)
            self.append(templ_descrip)


def op_template_get_argv(template_name):
    sub_command = "template"
    sub_cmd_args = ["get", template_name]

    argv_obj = _OPArgv.item_generic_argv('op', sub_command, sub_cmd_args)
    return argv_obj


class OPItemTemplateRegistry:

    REGISTRY_JSON = "template-registry.json"

    def __init__(self, template_dir):
        self.template_dir = Path(template_dir)
        self.registry_path = Path(template_dir, self.REGISTRY_JSON)
        self.registry = self._initialize_registry()

    def _initialize_registry(self):
        try:
            registry = json.load(open(self.registry_path, "r"))
        except FileNotFoundError:
            registry = {}
            self._write_registry(registry, self.registry_path)
        return registry

    def _write_registry(self, registry, registry_path):
        registry_path = Path(registry_path)
        registry_json = json.dumps(registry, indent=2)
        registry_path.write_text(registry_json)

    def add_template(self, item_name, item_json):
        template_filename = f"{item_name}.json"
        template_path = Path(self.template_dir, template_filename)
        template_obj = json.loads(item_json)
        category = template_obj["category"]
        template_path.write_text(item_json)
        self.registry[category] = template_filename
        self._write_registry(self.registry, self.registry_path)


def main():
    op: OP
    parsed = parse_args()

    try:
        op = do_signin(account=parsed.account)
    except OPSigninException as e:
        print("sign-in failed", file=sys.stderr)
        print(e.err_output, file=sys.stderr)
        exit(e.returncode)

    registry = OPItemTemplateRegistry(parsed.template_dir)
    template_list_argv = _OPArgv.item_template_list_argv('op')
    # using private APIs here. DON"T do this!
    template_list_json = op._run(
        template_list_argv, capture_stdout=True, decode="utf-8")
    template_list = OPItemTemplateDescriptorList(template_list_json)
    for template in template_list:
        normalized_name = template.normalized_name
        argv = op_template_get_argv(template.name)
        # SUPER internal & private API
        template_json = op._run(argv, capture_stdout=True, decode="utf-8")
        registry.add_template(normalized_name, template_json)


if __name__ == "__main__":
    main()
