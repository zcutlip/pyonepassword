import getpass

from pyonepassword import OP, logging
from pyonepassword._op_cli_config import OPCLIAccountConfig, OPCLIConfig
from pyonepassword._py_op_commands import (  # noqa: F401
    EXISTING_AUTH_AVAIL,
    EXISTING_AUTH_IGNORE,
    EXISTING_AUTH_REQD
)

logger = logging.console_logger(__name__, logging.DEBUG)

logger.debug("DEBUG logging enabled")
logger.info("INFO logging enabled")

config = OPCLIConfig()
account: OPCLIAccountConfig = config.account_map["zach_and_leanne"]
account_id = account.shorthand


password = None
if not OP.uses_biometric("op"):
    password = getpass.getpass("password:")

use_existing = EXISTING_AUTH_AVAIL
