import json
from pathlib import Path
from typing import Dict

from .paths import VALID_DATA_PATH, VALID_DATA_REGISTRY_PATH


class ValidData:
    REGISTRY_PATH = VALID_DATA_REGISTRY_PATH
    DATA_PATH = VALID_DATA_PATH

    def __init__(self, registry=None):
        if not registry:
            registry = json.load(open(self.REGISTRY_PATH, "r"))
        self._registry = registry
        self._data_path = self.DATA_PATH

    def _load_registry_dict(self, item_path):
        registry_path = Path(item_path, "registry.json")
        with open(registry_path, "r") as f:
            reg_dict = json.load(f)
        registry = {"data_path": item_path, "registry": reg_dict}
        return registry

    def _load_text_or_json(self, item_path, item_type, strip):
        if item_type in ["text", "json"]:
            mode = "r"
        else:
            mode = "rb"
        data = open(item_path, mode).read()
        if item_type == "json":
            data = json.loads(data)

        if strip:
            data = data.rstrip()
        return data

    def data_for_name(self, entry_name):
        entry: Dict = self._registry[entry_name]
        item_filename = entry["name"]
        item_type = entry["type"]
        strip = entry.get("strip", False)
        item_path = Path(self._data_path, item_filename)

        if item_type == "registry":
            data = self._load_registry_dict(item_path)
        else:
            data = self._load_text_or_json(item_path, item_type, strip)

        return data
