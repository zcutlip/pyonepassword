from pyonepassword import OP
from pyonepassword.api.object_types import OPLoginItem

from ..do_signin import do_signin

if __name__ == "__main__":
    # see README.md for sign-in process
    op: OP = do_signin()

    title = "Example Login Item"
    username = "test_username"
    great_password = "really-great-password"

    login_url = "https://website.example"

    new_item: OPLoginItem = op.login_item_create(title,
                                                 username,
                                                 url=login_url,
                                                 password=great_password,
                                                 vault="Test Data")
