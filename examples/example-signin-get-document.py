import getpass
import os
import sys
parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import (  # noqa: E402
    OP,
    OPSigninException,
    OPLookupException,
    OPNotFoundException
)


def do_signin():
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(prompt="1Password master password:\n")
    return OP(password=my_password)


if __name__ == "__main__":
    try:
        op = do_signin()
    except OPSigninException as opse:
        print("1Password sign-in failed.")
        print(opse.err_output)
        exit(opse.returncode)
    except OPNotFoundException as opnf:
        print("Uh oh. Couldn't find 'op'")
        print(opnf)
        exit(opnf.errno)

    print("Signed in.")
    print("Looking up \"Document\"...")
    try:
        # the document item often has a different 'fileName' attribute than
        # the document's name, so get_document() returns 1Password's fileName attribute
        # even though you already know the document name
        file_name, document_bytes = op.get_document("kessel - Shellcode.png")
        print(file_name)
        print("{} bytes".format(len(document_bytes)))
        print("")
        print("\"Document\" can also be looked up by its uuid")
        print("")
        print("Looking up uuid \"mzq5peufffhlhh6dn4hkj2twvm\"...")
        file_name, document_bytes = op.get_document(
            "mzq5peufffhlhh6dn4hkj2twvm")
        print(file_name)
        print("{} bytes".format(len(document_bytes)))
        print("Writing downloaded document to {}".format(file_name))
        open(file_name, "wb").write(document_bytes)
    except OPLookupException as ople:
        print("1Password lookup failed: {}".format(ople))
        print(ople.err_output)
        exit(ople.returncode)
    except OPNotFoundException as opnf:
        print("Uh oh. Couldn't find 'op'")
        print(opnf)
        exit(opnf.errno)
