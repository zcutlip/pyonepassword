from pyonepassword import OP, logging

logger = logging.console_logger("item-delete", logging.DEBUG)
op = OP(logger=logger)
vault = "Test Data"
item_name = "Delete Me Unique"
