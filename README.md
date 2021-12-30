# PYONEPASSWORD

## Description

A Python API to sign into and query a 1Password account using the `op` command.

## Requirements

- Python >= 3.8
- 1Password command-line tool
  - see [1Password command-line tool: Getting started](https://support.1password.com/command-line-getting-started/)
- Internet connectivity to 1Password.com
  - The `op` command queries your online account, not your local vault

## Installation

```shell
python3 -m pip install pyonepassword
```

## Example usage

> Note: It is recommended to perform initial sign-in manually on the command line before using `pyonepassword`. Initial sign-in is supported but deprecated. Multi-factor-authenticaiton is not supported.

### Subsequent sign-in and item retrieval

Below is an example demonstrating:

- Subsequent sign-in
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

## Notes

- You need the `op` 1Password command-line tool. On a Mac with homebrew, you can do `brew install 1password-cli`
  - More details [here](https://support.1password.com/command-line-getting-started/)
- For item creation, `op` v1.12.1 or higher is required
  - On earlier versions, an `OPCreateItemNotSupportedException` will be raised if on attempted item creation 

## TODO

- Ability for forget arbitrary accounts, not just the one currently signed in
- API mapping on to all of `op`'s various commands and subcommands
- API to get complete or partial JSON for an item
