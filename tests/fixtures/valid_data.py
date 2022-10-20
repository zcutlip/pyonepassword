import json
from pathlib import Path
from typing import Dict

from .paths import VALID_DATA_PATH, VALID_DATA_REGISTRY_PATH


class ValidData:
    REGISTRY_PATH = VALID_DATA_REGISTRY_PATH
    DATA_PATH = VALID_DATA_PATH

    def __init__(self):
        registry = json.load(open(self.REGISTRY_PATH, "r"))
        self._registry = registry

    def data_for_name(self, entry_name):
        entry: Dict = self._registry[entry_name]
        item_filename = entry["name"]
        item_type = entry["type"]
        strip = entry.get("strip", False)
        item_path = Path(self.DATA_PATH, item_filename)

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
