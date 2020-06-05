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

from pyonepassword import (  # noqa: E401
    OP,
    OPSigninException,
    OPGetDocumentException,
    OPInvalidDocumentException,
    OPNotFoundException
)


def do_signin():
    account_shorthand = "arbitrary_account_shorthand"
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(prompt="1Password master password:\n")
    return OP(account_shorthand, password=my_password)


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
    print("Getting document \"Example Login - 1Password Logo\"...")
    try:
        # the document item often has a different 'fileName' attribute than
        # the document's name, so get_document() returns 1Password's fileName attribute
        # even though you already know the document name
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
    except OPGetDocumentException as ope:
        # Couldn't find your document in 1Password
        print("1Password lookup failed: {}".format(ope))
        print(ope.err_output)
        exit(ope.returncode)
    except OPInvalidDocumentException as ope:
        # Found an item by name or UUID, but doesn't appear to represent a document object
        print("1Password item is not a valid document: {}".format(ope))
        exit(-1)
    except OPNotFoundException as opnf:
        print("Uh oh. Couldn't find 'op'")
        print(opnf)
        exit(opnf.errno)
