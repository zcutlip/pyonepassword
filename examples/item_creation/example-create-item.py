from pyonepassword import OP
from pyonepassword.api.object_types import OPLoginItem
from pyonepassword.op_items.password_recipe import (
    LETTERS_DIGITS_SYMBOLS_20,
    OPPasswordRecipe
)

if __name__ == "__main__":

    username = "test_username"
    title = "Test Login Item"

    op = OP()
    recipe = OPPasswordRecipe(length=40, digits=False, symbols=False)
    # or...
    recipe = LETTERS_DIGITS_SYMBOLS_20

    new_item: OPLoginItem = op.login_item_create(title,
                                                 username,
                                                 url="https://website.example",
                                                 password=recipe,
                                                 vault="Test Data")
    # pprint(new_item, indent=2)
    # new_item_2 = op.login_item_create("New Login 2",
    #                                   "new_user_2",
    #                                   url="https://website.example",
    #                                   password="correct-horse-battery-staple",
    #                                   vault="Test Data")
    # pprint(new_item_2, indent=2)
