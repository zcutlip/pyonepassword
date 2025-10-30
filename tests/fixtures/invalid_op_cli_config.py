import os

from .invalid_data import InvalidData
from .valid_op_cli_config import ValidOPCLIConfig


class UnreadableOPCLIConfig(ValidOPCLIConfig):
    def __init__(self, config_path_type=None):
        super().__init__(config_path_type=config_path_type)
        os.chmod(self._op_config_path, 0o000)


class MissingOPCLIConfig(ValidOPCLIConfig):
    def __init__(self, config_path_type=None):
        super().__init__(config_path_type=config_path_type)
        os.unlink(self._op_config_path)


class MalformedOPCLIConfig(ValidOPCLIConfig):
    def __init__(self):
        invalid_data = InvalidData()
        malformed_config_text = invalid_data.data_for_name(
            "malformed-op-config-json")
        super().__init__(config_text=malformed_config_text)
