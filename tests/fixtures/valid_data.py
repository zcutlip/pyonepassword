import json
import os
import re
import shutil
from pathlib import Path
from typing import Dict

from .paths import VALID_DATA_PATH, VALID_DATA_REGISTRY_PATH


class ValidData:
    REGISTRY_PATH = VALID_DATA_REGISTRY_PATH
    DATA_PATH = VALID_DATA_PATH

    def __init__(self, registry=None):
        self._registry_path = None
        if not registry:
            registry = json.load(open(self.REGISTRY_PATH, "r"))
            self._registry_path = self.REGISTRY_PATH
        self._registry = registry
        self._data_path = self.DATA_PATH

    def _load_registry_dict(self, item_path):
        registry_path = Path(item_path, "registry.json")
        with open(registry_path, "r") as f:
            reg_dict = json.load(f)
        registry = {"data_path": item_path,
                    "registry": reg_dict, "registry_path": registry_path}
        return registry

    def _load_data_from_file(self, item_path, item_type, strip):
        if item_type in ["text", "json"]:
            mode = "r"
        else:
            strip = False
            mode = "rb"
        data = open(item_path, mode).read()
        if item_type == "json":
            data = json.loads(data)

        if strip:
            data = data.rstrip()
        return data

    def data_for_name(self, entry_name, version=0):
        entry: Dict = self._registry[entry_name]
        if "versions" in entry:
            entry = entry["versions"][version]

        item_filename = entry["name"]
        item_type = entry["type"]
        strip = entry.get("strip", False)
        item_path = Path(self._data_path, item_filename)

        if item_type == "registry":
            data = self._load_registry_dict(item_path)
        else:
            # text, json, binary
            data = self._load_data_from_file(item_path, item_type, strip)

        return data

    def _detect_indent(self):
        indent = None
        # split input into separate lines
        lines = open(self._registry_path, "r").readlines()
        # we've got to have at least two lines
        if len(lines) >= 2:
            second_line = lines[1]
            # presumably 2nd line is indented exactly one level
            match = re.match(r"^(\s+).+", second_line)
            if match:
                # grab the actual indentation blob
                indent = match.groups()[0]
            # if we didn't find a match, return None
            # and let the caller decide what to do
        return indent

    def sort_registry_to_disk(self):
        indent = self._detect_indent()
        registry = dict(sorted(self._registry.items(),
                        key=lambda item: item[0]))
        registry_path_tmp = f"{self._registry_path}.tmp"
        print(f"Moving {self._registry_path} to {registry_path_tmp}")
        shutil.move(self._registry_path, registry_path_tmp)

        try:
            print(f"Writing to {self._registry_path}")
            with open(self._registry_path, "w") as f:
                json.dump(registry, f, indent=indent)
        except Exception as e:
            print(f"Restoring {self._registry_path} from {registry_path_tmp}")
            shutil.move(registry_path_tmp, self._registry_path)
            raise e
        print(f"Deleting {registry_path_tmp}")
        os.unlink(registry_path_tmp)
