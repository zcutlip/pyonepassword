from pyonepassword import OP
from pyonepassword.api.constants import LETTERS_DIGITS_SYMBOLS_20
from pyonepassword.api.object_types import OPLoginItem, OPPasswordRecipe

from ..do_signin import do_signin

if __name__ == "__main__":
    # see README.md for sign-in process
    op: OP = do_signin()

    title = "Example Login Item"
    username = "test_username"
    login_url = "https://website.example"

    # Explicitly specify a recpie
    # in this case, a 40-character alphabetic-only password
    recipe = OPPasswordRecipe(length=40, digits=False, symbols=False)
    # ... or use one of the predefined constants (pyonepassword.api.constants)
    # 20-character letters/digits/symbols password
    recipe = LETTERS_DIGITS_SYMBOLS_20

    new_item: OPLoginItem = op.login_item_create(title,
                                                 username,
                                                 url=login_url,
                                                 # If 'password' is a recipe rather than a string
                                                 # the '--generate-password=<recipe>' CLI option will be used
                                                 # to auto-generate a password for this login item
                                                 password=recipe,
                                                 vault="Test Data")
