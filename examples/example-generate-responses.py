import getpass
import os
import sys

from mock_cli.responses import CommandInvocation, ResponseDirectory
parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import (  # noqa: E402
    OPResponseGenerator)


def do_signin():
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(prompt="1Password master password:\n")
    # You may optionally provide an account shorthand if you used a custom one during initial sign-in
    # shorthand = "arbitrary_account_shorthand"
    # return OP(account_shorthand=shorthand, password=my_password)
    # Or we'll try to look up account shorthand from your latest sign-in in op's config file
    return OPResponseGenerator(password=my_password)


def do_get_item_1(op: OPResponseGenerator):
    query_name = "get-item-[example-login-1]-[vault-test-data]"
    invocation: CommandInvocation = op.get_item_generate_response(
        "Example Login 1", query_name, vault="Test Data")
    return invocation


# def do_get_item_2(op: OPResponseGenerator, qd: OPQueryDict):
#     item_uuid = "nok7367v4vbsfgg2fczwu4ei44"
#     query_response: OPQueryResponse = op.get_item_generate_response(item_uuid)

#     query_name = "get-item-[example-login-2]"
#     qd.add_query(query_response, query_name)


# def do_get_item_3(op: OPResponseGenerator, qd: OPQueryDict):
#     item_uuid = "nok7367v4vbsfgg2fczwu4ei44"
#     query_response: OPQueryResponse = op.get_item_generate_response(
#         item_uuid, fields="username,password")

#     query_name = "get-item-[example-login-2]-[fields-username-password]"
#     qd.add_query(query_response, query_name)


# def do_get_document(op: OPResponseGenerator, qd: OPQueryDict):
#     document_name = "Example Login 2 - 1200px-SpongeBob_SquarePants_character.svg.png.webp"
#     response: OPQueryResponse = op.get_document_generate_response(
#         document_name)
#     qd.add_query(response, "get-document-[spongebob image]")


def do_get_invalid_item(op: OPResponseGenerator):
    item_name = "Invalid Item"
    query_name = "get-item-[invalid-item]"
    invocation: CommandInvocation = op.get_item_generate_response(item_name, query_name)
    return invocation


if __name__ == "__main__":
    op = do_signin()
    directory_path = "./response-directory.json"
    resopnse_dir = "./responses"
    directory = ResponseDirectory(directory_path, create=True, response_dir=resopnse_dir)
    invocation = do_get_item_1(op)
    directory.add_command_invocation(invocation, save=True)

    # do_get_item_2(op, query_dict)

    # do_get_item_3(op, query_dict)

    # do_get_document(op, query_dict)
    invocation = do_get_invalid_item(op)
    directory.add_command_invocation(invocation, save=True)
