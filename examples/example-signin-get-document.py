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
    OPConfigNotFoundException,
    OPGetDocumentException,
    OPInvalidDocumentException,
    OPNotFoundException,
    OPNotSignedInException,
    OPSigninException
)


def do_signin():
    # op_path = "op-binaries/2.0.0/op"
    op_path = "op"
    uses_biometric = OP.uses_biometric(op_path=op_path)
    try:
        op = OP(op_path=op_path,
                use_existing_session=True, password_prompt=False)
    except OPNotSignedInException as e:
        if uses_biometric:
            raise e
        # If you've already signed in at least once, you don't need to provide all
        # account details on future sign-ins. Just master password
        my_password = getpass.getpass(prompt="1Password master password:\n")
        # You may optionally provide an account shorthand if you used a custom one during initial sign-in
        # shorthand = "arbitrary_account_shorthand"
        # return OP(account_shorthand=shorthand, password=my_password)
        # Or we'll try to look up account shorthand from your latest sign-in in op's config file
        op = OP(password=my_password)
    return op


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
