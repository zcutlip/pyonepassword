import json
from pathlib import Path

from .paths import INVALID_DATA_PATH, INVALID_DATA_REGISTRY_PATH


class InvalidData:

    def __init__(self):
        registry = json.load(open(INVALID_DATA_REGISTRY_PATH, "r"))
        self._registry = registry

    def data_for_name(self, entry_name):
        entry = self._registry[entry_name]
        item_filename = entry["name"]
        item_type = entry["type"]
        item_path = Path(INVALID_DATA_PATH, item_filename)

        if item_type == "text":
            mode = "r"
        else:
            mode = "rb"
        data = open(item_path, mode).read()
        return data
