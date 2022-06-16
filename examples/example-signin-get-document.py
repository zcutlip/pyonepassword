import os
import sys

from do_signin import do_signin

parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
# isort: split
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword.api.exceptions import (  # noqa: E402
    OPConfigNotFoundException,
    OPDocumentGetException,
    OPInvalidDocumentException,
    OPNotFoundException,
    OPSigninException
)

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
    except OPConfigNotFoundException as ope:
        print("Didn't provide an account shorthand, and we couldn't locate 'op' config to look it up.")
        print(ope)
        exit(1)

    print("Signed in.")
    print("Getting document \"Example Login - 1Password Logo\"...")
    try:
        # the document item often has a different 'fileName' attribute than
        # the document's name, so get_document() returns 1Password's fileName attribute
        # even though you already know the document name
        file_name, document_bytes = op.document_get(
            "Example Login - 1Password Logo")
        print("The original file name and the document title in 1Password are often different.")
        print("File name: {}".format(file_name))
        print("Size: {} bytes".format(len(document_bytes)))
        print("")
        print("\"Example Login - 1Password Logo\" can also be looked up by its uuid")
        print("")
        print("Looking up uuid \"ue6i3anfk7vdzf6vntruaunbuy\"...")
        file_name, document_bytes = op.document_get(
            "ue6i3anfk7vdzf6vntruaunbuy")
        print(file_name)
        print("{} bytes".format(len(document_bytes)))
        print("Writing downloaded document to {}".format(file_name))
        open(file_name, "wb").write(document_bytes)
    except OPDocumentGetException as ope:
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
