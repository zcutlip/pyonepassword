# PYONEPASSWORD ITEM CREATION

## Description

This document describes the process of item creation using `pyonpassword`, as well as several relevant classes.

## Basic item creation

In the simplest case, use a convenience method on a signed-in `OP` object. Currently there is one for creating login items, but more will be added over time.

```python

from pyonepassword.api.object_types import

def main():
    # see README.md for sign-in process
  	op = do_signin()

    title = "Example Login Item"
    username = "test_username"
    great_password="really-great-password"

    login_url = "https://website.example"


    new_item: OPLoginItem = op.login_item_create(title,
                                                 username,
                                                 url=login_url,
                                                 password=great_password,
                                                 vault="Test Data")

    recipe = OPPasswordRecipe(length=40, digits=False, symbols=False)
    # or...
    recipe = LETTERS_DIGITS_SYMBOLS_20
```
