from pyonepassword import OP, logging
from pyonepassword.api.exceptions import OPCmdFailedException  # noqa: F401

logger = logging.console_logger("item-delete", logging.DEBUG)
op = OP(logger=logger, op_path="mock-op")
vault = "Test Data"
item_name = "Delete Me Unique"
