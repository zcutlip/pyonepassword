# PYONEPASSWORD

## Description

A Python API to sign into and query a 1Password account using the `op` command.

## Requirements

- Python >= 3.7
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


if __name__ == "__main__":
    try:
        op = do_signin()
    except OPSigninException as opse:
        print("1Password sign-in failed.")
        print(opse.err_output)
        exit(opse.returncode)
    except OPNotFoundException as ope:
        print("Uh oh. Couldn't find 'op'")
        print(ope)
        exit(ope.errno)
    except OPConfigNotFoundException as ope:
        print("Didn't provide an account shorthand, and we couldn't locate 'op' config to look it up.")
        print(ope)
        exit(1)

    print("Signed in.")
    print("Looking up \"Example Login\"...")
    try:
        item_password = op.get_item_password("Example Login")
        print(item_password)
        print("")
        print("\"Example Login\" can also be looked up by its uuid")
        print("")
        print("Looking up uuid \"ykhsbhhv2vf6hn2u4qwblfrmg4\"...")
        print("Overriding \"Test Data\" vault, and look in \"Private\" instead")
        item_password = op.get_item_password(
            "ykhsbhhv2vf6hn2u4qwblfrmg4", vault="Private")
        print(item_password)
    except OPGetItemException as ope:
        print("1Password lookup failed: {}".format(ope))
        print(ope.err_output)
        exit(ope.returncode)
    except OPNotFoundException as ope:
        print("Uh oh. Couldn't find 'op'")
        print(ope)
        exit(ope.errno)

```

```Console
$ python3 ./examples/example-signin-get-item.py
1Password master password:

Using account shorthand found in op config: my_1p_account
Doing normal (non-initial) 1Password sign-in
Signed in.
Looking up "Example Login"...
doth-parrot-hid-tussock-veldt

"Example Login" can also be looked up by its uuid

Looking up uuid "ykhsbhhv2vf6hn2u4qwblfrmg4"...
Overriding "Archive" vault, and look in "Private" instead
doth-parrot-hid-tussock-veldt
```

### Document retrieval

Below is an example demonstrating:

- Retrieving a document and its file name from 1Password, based on item name
- Retrieving a document & file name from 1Password, based on UUID

```Python
op = do_signin()
    file_name, document_bytes = op.get_document(
    "Example Login - 1Password Logo")
print("The original file name and the document title in 1Password are often different.")
print("File name: {}".format(file_name))
print("Size: {} bytes".format(len(document_bytes)))
print("")
print("\"Example Login - 1Password Logo\" can also be looked up by its uuid")
print("")
print("Looking up uuid \"bmxpvuthureo7e52uqmvqcr4dy\"...")
file_name, document_bytes = op.get_document(
    "bmxpvuthureo7e52uqmvqcr4dy")
print(file_name)
print("{} bytes".format(len(document_bytes)))
print("Writing downloaded document to {}".format(file_name))
open(file_name, "wb").write(document_bytes)
```

```Console
$ python3 ./examples/example-signin-get-document.py
1Password master password:

Doing normal (non-initial) 1Password sign-in

Signed in.
Getting document "Example Login - 1Password Logo"...
The original file name and the document title in 1Password are often different.
File name: logo-v1.svg
Size: 2737 bytes

"Example Login - 1Password Logo" can also be looked up by its uuid

Looking up uuid "bmxpvuthureo7e52uqmvqcr4dy"...
logo-v1.svg
2737 bytes
Writing downloaded document to logo-v1.svg
```

### Signing out of 1Password

Below is an example demonstrating:

- Signing in, then signing out of 1Password
- Signing out and also forgetting a 1Password account

> Note: Currently `pyonepassword`'s sign-out & forget support requires a signed-in session. It is not yet possible to forget an arbitrary account.

```Python
def do_lookup():
    try:
        print(op.get_item_password("Example Login"))
    except OPGetItemException as opge:
        print("Get item failed.")
        print(opge.err_output)
        return opge.returncode


if __name__ == "__main__":
    try:
        op = do_signin()
    except OPSigninException as opse:
        print("1Password sign-in failed.")
        print(opse.err_output)
        exit(opse.returncode)

    print("Doing signout.")
    try:
        op.signout()
    except OPSignoutException as e:
        print("Signout failed.")
        print(e.err_output)
        exit(e.returncode)

    print("Trying to get item")
    do_lookup()

    print("Trying 'op forget'")
    try:
        op = do_signin()
    except OPSigninException as opse:
        print("1Password sign-in failed.")
        print(opse.err_output)
        exit(opse.returncode)

    print("Doing forget.")
    try:
        op.signout(forget=True)
    except OPSignoutException as e:
        print(e.err_output)
        exit(e.returncode)
    print("Done.")

    print("Trying to get item")
    ret = do_lookup()

    print("Trying to re-signin")
    try:
        do_signin()
    except OPSigninException as opse:
        print("1Password sign-in failed.")
        print(opse.err_output)
```

```console
$ python3 ./examples/example-signin-signout.py
1Password master password:

Using account shorthand found in op config: my_1p_account
Doing normal (non-initial) 1Password sign-in
Doing signout.
Trying to get item
Get item failed.
[ERROR] 2020/10/23 11:32:55 You are not currently signed in. Please run `op signin --help` for instructions
Trying 'op forget'
1Password master password:

Using account shorthand found in op config: my_1p_account
Doing normal (non-initial) 1Password sign-in
Doing forget.
Done.
Trying to get item
Get item failed.
[ERROR] 2020/10/23 11:33:04 The account details you entered aren't saved on this device. Use `op signin` to sign in to an account.
Trying to re-signin
1Password master password:

Using account shorthand found in op config:
Doing normal (non-initial) 1Password sign-in
1Password sign-in failed.
[ERROR] 2020/10/23 11:33:11 No account found on this device.

To sign in to an account: op signin --help
```

### Getting Details for a User

```Python
op = OP(password=my_password)

# User's name:
user_dict = op.get_user("Firstname Lastname")

# or the user's UUID
user_dict = op.get_user(user_uuid)
```

### Getting Details for a Group

```Python
op = OP(password=my_password)

# Group name:
group_dict = op.get_group("Team Members")

# or the group's UUID
group_dict_ = op.get_group("yhdg6ovhkjcfhn3u25cp2bnl6e")
```

### Getting Details for a Vault

```Python
op = OP(password=my_password)

# Group name:
vault_dict = op.get_vault("Test Data")

# or the group's UUID
vault_dict = op.get_vault("yhdg6ovhkjcfhn3u25cp2bnl6e")
```

## Notes

- This has been lightly tested, and only on my Mac. I don't know if it works on other systems.
- This has been tested with `op` version 1.7.0
- You need the `op` 1Password command-line tool. On a Mac with homebrew, you can do `brew install 1password-cli`.

## TODO

- Ability for forget arbitrary accounts, not just the one currently signed in
- API mapping on to all of `op`'s various commands and subcommands
- API to get complete or partial JSON for an item
- Unit testing
