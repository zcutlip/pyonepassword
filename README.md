# PYONEPASSWORD

## Description

A Python API to sign into and query a 1Password account using the `op` command.

## Requirements

- Python >= 3.8
- 1Password command-line tool >= 2.0.0
  - see [1Password Developer Documentation](https://developer.1password.com/docs/cli)
- Internet connectivity to 1Password.com
  - The `op` command queries your online account, not your local vault

> Note: This version of `pyonepassword` does not support deprecated `op` 1.x versions. Support for those versions is still available, albeit with minimal maintanence. See [pyonepassword-legacy](https://github.com/zcutlip/pyonepassword-legacy) for more information.

## A Quick Favor

I don't have a way of knowing how widely this project is used. If you're using it, I would love for you to drop me a tweet ([@zcutlip](https://twitter.com/zcutlip)) or an email (see the commit history) and let me know. I'm interested in how it's going for you, how you're using it (if you're able to share), if there are things that are working well or not working well, etc.

## Installation

```shell
python3 -m pip install pyonepassword
```

## Example Usage

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
        except OPNotSignedInException:
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

### More Examples

Lots more examples are available in the `examples` directory
