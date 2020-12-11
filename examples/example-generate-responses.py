# noqa: E402
import getpass
import os
import sys
import json
from pathlib import Path
parent_path = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
if parent_path not in sys.path:
    sys.path.append(parent_path)

from pyonepassword import OPResponseGenerator, OPQueryResponse  # noqa: E402


def do_signin():
    # If you've already signed in at least once, you don't need to provide all
    # account details on future sign-ins. Just master password
    my_password = getpass.getpass(prompt="1Password master password:\n")
    # You may optionally provide an account shorthand if you used a custom one during initial sign-in
    # shorthand = "arbitrary_account_shorthand"
    # return OP(account_shorthand=shorthand, password=my_password)
    # Or we'll try to look up account shorthand from your latest sign-in in op's config file
    return OPResponseGenerator(password=my_password)


def do_get_item_1(op):
    response: OPQueryResponse = op.get_item_generate_response(
        "Example Login 1", vault="Test Data")

    response_path = Path(
        "responses", "get-item-[example-login-1]-[vault-test-data].json")
    response_dict = response.record_response(response_path)
    return response_dict


def do_get_item_2(op: OPResponseGenerator):
    item_uuid = "nok7367v4vbsfgg2fczwu4ei44"
    response: OPQueryResponse = op.get_item_generate_response(item_uuid)

    response_path = Path(
        "responses", "get-item-[example-login-2].json")
    response_dict = response.record_response(response_path)
    return response_dict


def do_get_item_3(op: OPResponseGenerator):
    item_uuid = "nok7367v4vbsfgg2fczwu4ei44"
    response: OPQueryResponse = op.get_item_generate_response(
        item_uuid, fields="username,password")

    response_path = Path(
        "responses", "get-item-[example-login-2]-[fields-username-password].json")
    response_dict = response.record_response(response_path)
    return response_dict


def do_get_document(op: OPResponseGenerator):
    document_name = "Example Login 2 - 1200px-SpongeBob_SquarePants_character.svg.png.webp"
    response: OPQueryResponse = op.get_document_generate_response(
        document_name)
    response_path = Path("responses", "get-document-[spongebob image].webp")
    response_dict = response.record_response(response_path)

    return response_dict


if __name__ == "__main__":
    op = do_signin()

    query_list = []
    response_dict = do_get_item_1(op)
    query_list.append(response_dict)

    response_dict = do_get_item_2(op)
    query_list.append(response_dict)

    response_dict = do_get_item_3(op)
    query_list.append(response_dict)

    response_dict = do_get_document(op)
    query_list.append(response_dict)

    query_dict = {
        "queries": query_list
    }
    json.dump(query_dict, open("op_queries.json", "w"), indent=2)
