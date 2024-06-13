from pyonepassword import OP, logging
from pyonepassword.api.object_types import OPLoginItem

if __name__ == "__main__":
    # see README.md for sign-in process
    logger = logging.console_debug_logger("example-create-item")
    op: OP = OP(logger=logger)
    title = "Example Login Item"
    username = "test_username"
    great_password = "really-great-password"

    login_url = "https://website.example"

    new_item: OPLoginItem = op.login_item_create(title,
                                                 username,
                                                 url=login_url,
                                                 password=great_password,
                                                 vault="Test Data")
