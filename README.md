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

### Subsequent sign-in and lookup

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
    print("Signed in.")
    print("Looking up \"Example Login\"...")
    print(op.lookup("Example Login"))
    print("")
    print("\"Example Login\" can also be looked up by its uuid")
    print("")
    print("Looking up uuid \"ykhsbhhv2vf6hn2u4qwblfrmg4\"...")
    print(op.lookup("ykhsbhhv2vf6hn2u4qwblfrmg4"))
    print("Downloading file \"ehhvhlcsakrp28lefy7hsr7lqy\"...")
    print(op.download("ehhvhlcsakrp28lefy7hsr7lqy"))
```

```console
$ python3 ./examples/example-signin-lookup.py
1Password master password:

Doing normal (non-initial) 1Password sign-in

Signed in.
Looking up "Example Login"...
doth-parrot-hid-tussock-veldt

"Example Login" can also be looked up by its uuid

Looking up uuid "ykhsbhhv2vf6hn2u4qwblfrmg4"...
doth-parrot-hid-tussock-veldt
```

## Notes

- This has been lightly tested, and only on my Mac. I don't know if it works on other systems.
- This has been tested with `op` version 0.5.6.
- You need the `op` 1Password command-line tool. On a Mac with homebrew, you can do `brew install 1password-cli`.

## TODO

- Detect if `op` is/is not installed, and be helpful
- API to get complete or partial JSON for a vault item, not just a specific field's value
- Maybe one day 1Password.com will have an API and this module won't have to use `op`
