import os

from pyonepassword import OP, logging
from pyonepassword._op_cli_config import OPCLIAccountConfig, OPCLIConfig
from pyonepassword._op_commands import (  # noqa: F401
    EXISTING_AUTH_AVAIL,
    EXISTING_AUTH_IGNORE,
    EXISTING_AUTH_REQD
)

"""
Basic ipython bootstrap script for using the OP class
"""

logger = logging.console_logger(__name__, logging.DEBUG)

logger.debug("DEBUG logging enabled")
logger.info("INFO logging enabled")

os.environ['LOG_OP_ERR'] = "1"
