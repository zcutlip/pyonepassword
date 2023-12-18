# PYONEPASSWORD

![PyPI - Version](https://img.shields.io/pypi/v/pyonepassword)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyonepassword)
![Testing & linting](https://github.com/zcutlip/pyonepassword/actions/workflows/python-package.yml/badge.svg)
![CodeQL](https://github.com/zcutlip/pyonepassword/actions/workflows/codeql.yml/badge.svg)



## Description

A Python API to sign into and query a 1Password account using the `op` command.

## Requirements

- Python >= 3.9
- 1Password command-line tool >= 2.0.0
  - see [1Password Developer Documentation](https://developer.1password.com/docs/cli)
- Internet connectivity to 1Password.com
  - The `op` command queries your online account, not your local vault

> Note: This version of `pyonepassword` does not support deprecated `op` 1.x versions. Support for those versions is still available, albeit with minimal maintanence. See [pyonepassword-legacy](https://github.com/zcutlip/pyonepassword-legacy) for more information.

## Installation

```shell
python3 -m pip install pyonepassword
```

## Overview

`pyonepassword` essentially has two parts:

1. Convenience Python classes for the various objects that the `op` command returns
2. A full-fledged API for querying a 1Password account

If you already have a workflow to drive the `op` command, handle authentication, and so forth, but would benefit from an API that can ingest `op`'s JSON and give you Python objects, you're in luck, number one might be just what you need.

On the other hand, if you're using `op` manually (maybe along side `jq`), or in shell scripts (or maybe not at all), and you'd like a full-service Python API rather than console commands, number two does that.

We'll get into some examples below for both of these.



## Example Usage

### Object API

`pyonepassword` provides Python classes for many of the objects `op` returns, including:

- Several "item" types (login, password, secure note, etc)
- User
- User List (e.g., from 'op user list')
- Group
- Group List
- Vault
- Vault List
- Account
- Account List

All of these classes provide assorted convenience properties. For example `obj.created_at` returns a proper Python `datetime` object.

All of the object types are fundamentally dictionaries, so their data can be accessed as such, and they can be serialized back to JSON.

Also, all classes can be instantiated from either directly from a JSON string, or from an unserialized object.

Take the following Login item as an example:

```JSON
{
  "id": "4smjvvepfbg3hencrmo7cozphe",
  "title": "Example Login",
  "version": 2,
  "vault": {
    "id": "yhdg6ovhkjcfhn3u25cp2bnl6e"
  },
  "category": "LOGIN",
  "last_edited_by": "RAXCWKNRRNGL7I3KSZOH5ERLHI",
  "created_at": "2021-06-29T18:42:03Z",
  "updated_at": "2022-03-17T03:40:49Z",
  "sections": [
    {
      "id": "linked items",
      "label": "Related Items"
    }
  ],
  "fields": [
    {
      "id": "password",
      "type": "CONCEALED",
      "purpose": "PASSWORD",
      "label": "password",
      "value": "doth-parrot-hid-tussock-veldt",
      "password_details": {
        "strength": "FANTASTIC"
      }
    },
    {
      "id": "username",
      "type": "STRING",
      "purpose": "USERNAME",
      "label": "username",
      "value": "zcutlip"
    },
    {
      "id": "notesPlain",
      "type": "STRING",
      "purpose": "NOTES",
      "label": "notesPlain"
    }
  ],
  "urls": [
    {
      "href": "http://example2.website"
    },
    {
      "primary": true,
      "href": "https://example.website"
    }
  ]
}
```

In just a line of Python, you can create an `OPLoginItem` object:

```Python

from pyonepassword.api.object_types import OPLoginItem

login_item = OPLoginItem(login_item_json)


print(login_item.username)
print(login_item.password)
print(login_item.primary_url.href)

# login_item is also a dictionary:
print(login_item["username"] == login_item.username)
```

### Example usage of the `OP` class

If you want to fully automate connecting to and querying a 1Password account, that's what the `OP` class is for. It handles authentication (except for initial sign-in). And provides methods that are congruent to many of the `op` CLI tool's subcommands, such as:

- `item_get()`
- `item_list()`
- `user_get()`
- `user_list()`...

... and so forth.

All of these methods return objects types as described above. Also, `item_get()` returns the appropriate object type for the item, such as `OPLoginItem` or `OPSecureNoteItem`, as long as `pyonepassword` has a class for the returned item type.

> *Note*: In some cases the `op` command may return items that don't conform to the expected structure. When this happens, the item dictionary will fail to validate, an exception will be raised. There is API for relaxing item validation, globally, on a per-class basis, or a per-item basis. See [item-validation.md](docs/item-validation.md) for more information.

### Sign-in and item retrieval

Below is an example demonstrating:

- Sign-in
- Specifying a default vault for queries
- Retrieving an item from 1Password by name or by UUID
- Overriding the default vault to retrieve a subsequent item from 1Password

```Python
import getpass

from pyonepassword import OP
from pyonepassword.api.exceptions import (
    OPSigninException,
    OPItemGetException,
    OPNotFoundException,
    OPConfigNotFoundException
)



# See examples/example-sign-in.py for more sign-in examples
def do_signin():
    # Let's check If biometric is enabled
    # If so, no need to provide a password
    if OP.uses_biometric():
        try:
            # no need to provide any authentication parameters if biometric is enabled
            op = OP()
        except OPAuthenticationException:
            print("Uh oh! Sign-in failed")
            exit(-1)
    else:
        # prompt user for a password (or get it some other way)
        my_password = getpass.getpass(prompt="1Password master password:\n")
        # You may optionally provide an account shorthand if you used a custom one during initial sign-in
        # shorthand = "arbitrary_account_shorthand"
        # return OP(account_shorthand=shorthand, password=my_password)
        # Or we'll try to look up account shorthand from your latest sign-in in op's config file
        op = OP(password=my_password)
    return op


def main():
  	op = do_signin()
    item_password = op.item_get_password("Example Login")

    # We can also look up the item by its UUID
    # as well as retrieve from an alternate vault
    item_password = op.item_get_password(
      "ykhsbhhv2vf6hn2u4qwblfrmg4", vault="Private")

```

### Document retrieval

Below is an example demonstrating:

- Retrieving a document and its file name from 1Password, based on item name
- Retrieving a document & file name from 1Password, based on UUID

```Python
op = do_signin()
# File name and document title in 1Password are often different.
# so we get back the file name, and the bytes object representing the document
file_name, document_bytes = op.document_get("Example Login - 1Password Logo")

# we can also look up the document by UUID
file_name, document_bytes = op.document_get(
    "bmxpvuthureo7e52uqmvqcr4dy")
open(file_name, "wb").write(document_bytes)
```

### Signing out of 1Password

Below is an example demonstrating:

- Signing in, then signing out of 1Password
- Signing out and also forgetting a 1Password account

> Note: Currently `pyonepassword`'s sign-out & forget support requires a signed-in session. It is not yet possible to forget an arbitrary account.

```Python
def main():
	  op = do_signin()

    # do signout
    op.signout()

    try:
		    print(op.item_get_password("Example Login"))
     except OPItemGetException:
      	# lookup fails since we signed out
        pass

    # now let's sign in again, then signout with forget=True
    op = do_signin()
    op.signout(forget=True)

    try:
        do_signin()
    except OPSigninException:
				# Sign-in fails since we erased the initial sign-in with forget=True
				pass
```

### Getting Details for a User

```Python
op = OP(password=my_password)

# User's name:
user: OPUser = op.user_get("Firstname Lastname")

# or the user's UUID
user: OPUser = op.user_get(user_uuid)
```

### Getting Details for a Group

```Python
op = OP(password=my_password)

# Group name:
group: OPGroup = op.group_get("Team Members")

# or the group's UUID
group: OPGroup = op.group_get("yhdg6ovhkjcfhn3u25cp2bnl6e")
```

### Getting Details for a Vault

```Python
op = OP(password=my_password)

# Group name:
vault: OPVault = op.vault_get("Test Data")

# or the group's UUID
vault: OPVault = op.vault_get("yhdg6ovhkjcfhn3u25cp2bnl6e")
```

### Extending Item Types

If any of the item types (login, password, etc.) are missing or don't provide sufficient properties or methods, it's very easy to add new ones or extend existing ones.

Here's an example extending `OPLoginItem`.

```python
from pyonepassword import OP
from pyonepassword.api.decorators import op_register_item_type
from pyonepassword.api.object_types import OPLoginItem

@op_register_item_type
class OPEnhancedLoginItem(OPLoginItem):

    @property
    def custom_property(self):
      return self["custom_field"]


op = OP()
enhanced_login = op.item_get("Example Login", vault="Test Data")

print(enhanced_login.custom_property)
```

### Item Deletion

```Python

from pyonepassword import OP  # noqa: E402
from pyonepassword.api.exceptions import OPItemDeleteException  # noqa: E402


def main():
    op: OP()
    try:
        # op.item_delete() can take any identifier accepted by the 'op' command:
        # Usage:  op item delete [{ <itemName> | <itemID> | <shareLink> | - }] [flags]
        deleted_uuid = op.item_delete("Example Login")  # noqa: F841
        # if desired inspect resulting UUID to ensure it's what was
        # Expected
    except OPItemDeleteException as ope:
        # 'op' command can fail for a few reaons, including
        # - item not found
        # - duplicate item names
        # Inspect the error message from the command
        print(ope.err_output)
```


### Item Creation

For details on creating new items in a 1Password vault, see [item-creation.md](docs/item-creation.md)

Also see the examles in [examples/item_creation](examples/item_creation/)


### Item Editing

For details on editing existing items in a 1Password vault, see [item-editing.md](docs/item-editing.md)

Also see the examles in [examples/item_editing](examples/item_editing/)

### Document Editing

For details on editing existing document item file contents, see [document-editing.md](docs/document-editing.md)

See examples in [examples/document_editing](examples/document_editing.py)

### User Editing

User editing is supported via the `OP.user_edit()` method. It supports toggling travel mode on and off, as well as setting a new user name. Only one user at a time may be edited via this method.

See examples in [examples/user_editing](examples/user_editing.py)

### More Examples

Lots more examples are available in the `examples` directory
