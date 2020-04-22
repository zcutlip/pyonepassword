# PYONEPASSWORD

## Description

A Python API to sign into and query a 1Password account using the `op` command.

## Requirements

- Python >= 3.7
- 1Password command-line tool
  - see [1Password command-line tool: Getting started](https://support.1password.com/command-line-getting-started/)
- Internet connectivity to 1Password.com
  - The `op` command queries your online account, not your local vault

## Example usage

### Intitial sign-in

```Python
import getpass
from pyonepassword.pyonepassword import (
    OP,
    OPSigninException
)


def do_initial_signin():
    my_signin_address = "my-1p-account.1password.com"
    my_email_address = "my-1p-email@email.com"
    my_secret_key = getpass.getpass(prompt="1Password secret key:\n")
    my_password = getpass.getpass(prompt="1Password master password:\n")
    try:
        op = OP(signin_address=my_signin_address,
                email_address=my_email_address,
                secret_key=my_secret_key,
                password=my_password)
    except OPSigninException as ope:
        print("1Password initial signin failed: {}".format(ope))
        print(ope.err_output)
        exit(1)
    print("1Password is signed in and ready for lookups")
    return op


if __name__ == "__main__":
    op = do_initial_signin()
    # op is ready to use and call lookup() on
    print("Signed in.")
```

```Console
$ python3 ./example.py
1Password secret key:
1Password master password:
Performing initial 1Password sign-in to my-1p-account.1password.com as my-1p-email@email.com
Signed in.
```

### Subsequent sign-in and item retrieval

```Python
import getpass
from pyonepassword import (
    OP,
    OPSigninException
)
def do_signin():
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(prompt="1Password master password:\n")
    try:
        op = OP(password=my_password)
    except OPSigninException as ope:
        print("1Password initial signin failed: {}".format(ope))
        print(ope.err_output)
        exit(1)
    return op


if __name__ == "__main__":
    op = do_signin()
    item_password = op.get_item_password("Example Login")
    print(item_password)
    print("")
    print("\"Example Login\" can also be looked up by its uuid")
    print("")
    print("Looking up uuid \"ykhsbhhv2vf6hn2u4qwblfrmg4\"...")
    item_password = op.get_item_password("ykhsbhhv2vf6hn2u4qwblfrmg4")
    print(item_password)
```

```Console
$ python3 ./examples/example-signin-get-item.py
1Password master password:

Doing normal (non-initial) 1Password sign-in

Signed in.
Looking up "Example Login"...
doth-parrot-hid-tussock-veldt

"Example Login" can also be looked up by its uuid

Looking up uuid "ykhsbhhv2vf6hn2u4qwblfrmg4"...
doth-parrot-hid-tussock-veldt
```

### Document retrieval

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

## Notes

- This has been lightly tested, and only on my Mac. I don't know if it works on other systems.
- This has been tested with `op` version 0.5.6.
- You need the `op` 1Password command-line tool. On a Mac with homebrew, you can do `brew install 1password-cli`.

## TODO

- Detect if `op` is/is not installed, and be helpful
- API to get complete or partial JSON for a vault item, not just a specific field's value
- Maybe one day 1Password.com will have an API and this module won't have to use `op`
