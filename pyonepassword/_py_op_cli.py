import os
import pathlib
import json
from json.decoder import JSONDecodeError

from .py_op_exceptions import OPConfigNotFoundException

"""
Module to hold stuff that interacts directly with 'op' or its config

TODO: Move other code that closely touches 'op' here
"""


class OPCLIConfig(dict):
    OP_CONFIG_RELPATH = os.path.join(".op", "config")

    def __init__(self, configpath=None):
        super().__init__()
        if configpath is None:
            configpath = self._get_config_path()

        if configpath is None:
            raise OPConfigNotFoundException("No op configuration found")

        try:
            config_json = open(configpath, "r").read()
        except FileNotFoundError as e:
            raise OPConfigNotFoundException(
                "op config not found at path: {}".format(configpath)) from e
        except PermissionError as e:
            raise OPConfigNotFoundException(
                "Permission denied accessing op config at path: {}".format(configpath)) from e

        try:
            config = json.loads(config_json)
            self.update(config)
        except JSONDecodeError as e:
            raise OPConfigNotFoundException(
                "Unable to json decode config at path: {}".format(configpath)) from e

    def _get_config_path(self):
        try:
            xdg_path = os.environ['XDG_CONFIG_HOME']
            configpath = os.path.join(xdg_path, self.OP_CONFIG_RELPATH)
        except KeyError:
            configpath = None

        if configpath is None:
            configpath = os.path.join(
                pathlib.Path.home(), self.OP_CONFIG_RELPATH)

        return configpath
