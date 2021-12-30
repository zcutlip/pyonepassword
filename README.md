# PYONEPASSWORD

## Description

A Python API to sign into and query a 1Password account using the `op` command.

## Requirements

- Python >= 3.8
- 1Password command-line tool
  - see [1Password command-line tool: Getting started](https://support.1password.com/command-line-getting-started/)
- Internet connectivity to 1Password.com
  - The `op` command queries your online account, not your local vault

## A Quick Favor

I don't have a way of knowing how widely this project is used. If you're using it, I would love for you to drop me a tweet ([@zcutlip](https://twitter.com/zcutlip)) or an email (see the commit history) and let me know. I'm interested in how it's going for you, how you're using it (if you're able to share), if there are things that are working well or not working well, etc.

## Installation

```shell
python3 -m pip install pyonepassword
```

## Example usage

> Note: It is recommended to perform initial sign-in manually on the command line before using `pyonepassword`. Initial sign-in is supported but deprecated. Multi-factor-authenticaiton is not supported.

### A Note about Initial Sign-in

Initial sign-in, which was supported in earlier versions of `pyonepassword` is now deprecated. The reasons for this are:

- Use of multifactor authentication is highly encouraged for all users, but is not supported via `pyonepassword`
- If there was a way to perform mutlifactor authentication programatically, this would represent a failure of MFA; one of its main purposes is to capture user intent. If `pyonepassword` can automate MFA, so can malicious code.

Code that was previously relying on initial sign-in support in `pyonepassword`, must now be updated to continue workong. It is necessary to import a different, deprecated class. A one line change should allow existing code to continue working for the time being:

Change:

```python
from pyonepassword import OP
```

To:

```python
from pyonepassword import OP_ as OP
```

Other than deprecation warnings (via Python's `warnings.warn()`), everything should then function as normal. **Be aware that this functionality will be removed in a future update, without additional warning.**

### Sign-in and item retrieval

Below is an example demonstrating:

- Sign-in
- Specifying a default vault for queries
- Retrieving an item from 1Password by name or by UUID
- Overriding the default vault to retrieve a subsequent item from 1Password

```Python
import getpass

from pyonepassword import (  # noqa: E402
    OP,
    OPSigninException,
    OPGetItemException,
    OPNotFoundException,
    OPConfigNotFoundException
)


def do_signin():
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(prompt="1Password master password:\n")
    # You may optionally provide an account shorthand if you used a custom one during initial sign-in
    # shorthand = "arbitrary_account_shorthand"
    # return OP(account_shorthand=shorthand, password=my_password)
    # Or we'll try to look up account shorthand from your latest sign-in in op's config file
    return OP(vault="Test Data", password=my_password)


def main():
  	op = do_signin()
    item_password = op.get_item_password("Example Login")

  	# We can also look up the item by its UUID
    # as well as retrieve from an alternate vault
    item_password = op.get_item_password(
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
file_name, document_bytes = op.get_document("Example Login - 1Password Logo")

# we can also look up the document by UUID
file_name, document_bytes = op.get_document(
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
		    print(op.get_item_password("Example Login"))
     except OPGetItemException:
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
user: OPUser = op.get_user("Firstname Lastname")

# or the user's UUID
user: OPUser = op.get_user(user_uuid)
```

### Getting Details for a Group

```Python
op = OP(password=my_password)

# Group name:
group: OPGroup = op.get_group("Team Members")

# or the group's UUID
group: OPGroup = op.get_group("yhdg6ovhkjcfhn3u25cp2bnl6e")
```

### Getting Details for a Vault

```Python
op = OP(password=my_password)

# Group name:
vault: OPVault = op.get_vault("Test Data")

# or the group's UUID
vault: OPVault = op.get_vault("yhdg6ovhkjcfhn3u25cp2bnl6e")
```

## Item Creation

As of version 2.0, `pyonepassword` supports creation of entries in 1Password vaults. In order to do this, an "item template" class must be used that inherits from `OPItemTemplateMixin` along with one of the item classes (e.g., `OPLoginItem`). Currently, two classes are provided that do this: `OPLoginItemTemplate` and `OPServerItemTemplate`.

### Examples

Below are a couple of examples creating a login item.

### Creating a Login Item

The `OP` class provides a convenience method to create a login item.

```Python
op = do_signin()
username = "testuser"
password = "testpass"
url = "https://example.website"
item_name = "login 3"

result: OPLoginItem
result = op.create_login_item(item_name, username, password, url=url)
# result is an actual OPLoginItem object queried from 1Password after item creation
# Among other things it provides the UUID of the created object
print(f"Item UUID: {result.uuid}")
```

### Creating a Login Item with Custom Sections

Rather than use the convenience method, you may add custom sections and section fields to the item template before creation.

```python
newlogin = OPLoginItemTemplate(username, password)

# user-visible section title is required
# section name (not user visible) is optional and will be randomly generated if not provided
#                 section title -----v                 v-------- section name
# section = newlogin.add_section("New Section", "new_section")
section = newlogin.add_section("New Section")

# field name is not user visible
# field label is user visible
section.add_field("example field name", "example value", "string", "example field label")

op.create_item(newlogin, "login 3")
```



## Notes

- You need the `op` 1Password command-line tool. On a Mac with homebrew, you can do `brew install 1password-cli`
  - More details [here](https://support.1password.com/command-line-getting-started/)
- For item creation, `op` v1.12.1 or higher is required
  - On earlier versions, an `OPCreateItemNotSupportedException` will be raised if on attempted item creation 

## TODO

TODO list has moved to GitHub [Issues](https://github.com/zcutlip/pyonepassword/issues)

