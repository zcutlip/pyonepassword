import os

from pyonepassword import OP, logging
from pyonepassword._op_cli_config import OPCLIConfig
from pyonepassword._op_commands import EXISTING_AUTH_REQD
from tests.fixtures.op_fixtures import _setup_alt_env, _setup_normal_env
from tests.fixtures.valid_op_cli_config import (
    VALID_OP_CONFIG_NO_SHORTHAND_KEY,
    ValidOPCLIConfig
)

# _setup_alt_env()
# _setup_normal_env()
logger = logging.console_logger("pytest-misc", logging.DEBUG)

# config_obj = ValidOPCLIConfig(
#     valid_data_key=VALID_OP_CONFIG_NO_SHORTHAND_KEY)
# config = OPCLIConfig()
# shorthand = "NO_SUCH_SHORTHAND"
# conf = config.get_config(account_id=shorthand)

logger.debug(f"HOME: {os.environ['HOME']}")
op = OP(logger=logger)
