from typing import Dict

from .paths import BINARY_DATA_PATH, BINARY_DATA_REGISTRY_PATH
from .valid_data import ValidData


class BinaryData(ValidData):
    REGISTRY_PATH = BINARY_DATA_REGISTRY_PATH
    DATA_PATH = BINARY_DATA_PATH

    @property
    def binary_image_data(self) -> Dict[str, Dict]:
        item_data_registry = self.data_for_name("binary-image-data")
        return item_data_registry


class BinaryImageData(ValidData):

    def __init__(self):
        binary_data = BinaryData()
        binary_image_data_registry: Dict = binary_data.binary_image_data
        registry = binary_image_data_registry["registry"]
        super().__init__(registry=registry)
        self._data_path = binary_image_data_registry["data_path"]
        self._registry_path = binary_image_data_registry["registry_path"]

    def data_for_name(self, entry_name) -> bytes:
        data = super().data_for_name(entry_name)
        return data
