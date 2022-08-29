from .paths import INVALID_DATA_PATH, INVALID_DATA_REGISTRY_PATH
from .valid_data import ValidData


class InvalidData(ValidData):
    REGISTRY_PATH = INVALID_DATA_REGISTRY_PATH
    DATA_PATH = INVALID_DATA_PATH
