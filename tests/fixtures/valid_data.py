import json
from pathlib import Path

from .paths import VALID_DATA_PATH, VALID_DATA_REGISTRY_PATH


class ValidData:
    REGISTRY_PATH = VALID_DATA_REGISTRY_PATH
    DATA_PATH = VALID_DATA_PATH

    def __init__(self):
        registry = json.load(open(self.REGISTRY_PATH, "r"))
        self._registry = registry

    def data_for_name(self, entry_name):
        entry = self._registry[entry_name]
        item_filename = entry["name"]
        item_type = entry["type"]
        item_path = Path(self.DATA_PATH, item_filename)

        if item_type in ["text", "json"]:
            mode = "r"
        else:
            mode = "rb"
        data = open(item_path, mode).read()
        if item_type == "json":
            data = json.loads(data)
        return data
