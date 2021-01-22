import getpass
import os
import sys
import json
parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import (  # noqa: E402
    OPResponseGenerator,
    OPQueryResponse,
    OPQueryDict)


def do_signin():
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(prompt="1Password master password:\n")
    # You may optionally provide an account shorthand if you used a custom one during initial sign-in
    # shorthand = "arbitrary_account_shorthand"
    # return OP(account_shorthand=shorthand, password=my_password)
    # Or we'll try to look up account shorthand from your latest sign-in in op's config file
    return OPResponseGenerator(password=my_password)


def do_get_item_1(op: OPResponseGenerator, qd: OPQueryDict):
    query_response: OPQueryResponse = op.get_item_generate_response(
        "Example Login 1", vault="Test Data")
    qd.add_query(query_response,
                 "get-item-[example-login-1]-[vault-test-data]")


def do_get_item_2(op: OPResponseGenerator, qd: OPQueryDict):
    item_uuid = "nok7367v4vbsfgg2fczwu4ei44"
    query_response: OPQueryResponse = op.get_item_generate_response(item_uuid)

    query_name = "get-item-[example-login-2]"
    qd.add_query(query_response, query_name)


def do_get_item_3(op: OPResponseGenerator, qd: OPQueryDict):
    item_uuid = "nok7367v4vbsfgg2fczwu4ei44"
    query_response: OPQueryResponse = op.get_item_generate_response(
        item_uuid, fields="username,password")

    query_name = "get-item-[example-login-2]-[fields-username-password]"
    qd.add_query(query_response, query_name)


def do_get_document(op: OPResponseGenerator, qd: OPQueryDict):
    document_name = "Example Login 2 - 1200px-SpongeBob_SquarePants_character.svg.png.webp"
    response: OPQueryResponse = op.get_document_generate_response(
        document_name)
    qd.add_query(response, "get-document-[spongebob image]")


def do_get_invalid_item(op: OPResponseGenerator, qd: OPQueryDict):
    item_name = "Invalid Item"
    query_name = "get-item-[invalid-item]"
    query_response: OPQueryResponse = op.get_item_generate_response(item_name)
    qd.add_query(query_response, query_name)


if __name__ == "__main__":
    op = do_signin()

    query_dict = OPQueryDict("responses")
    do_get_item_3(op, query_dict)

    do_get_item_2(op, query_dict)

    do_get_item_3(op, query_dict)

    do_get_document(op, query_dict)
    do_get_invalid_item(op, query_dict)
    json.dump(query_dict, open("op_queries.json", "w"), indent=2)
