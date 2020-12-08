from ._py_op_commands import _OPCommandInterface
from ._py_op_cli import _OPArgv


class OPResponseGenerator(_OPCommandInterface):

    def _generate_response_dict(self, argv_obj, output, decode=None):
        if decode:
            binary = False
        else:
            binary = True
        query_dict = argv_obj.query_dict()

        resp_dict = {
            "response": output,
            "binary": binary
        }
        query_dict["response"] = resp_dict

        return resp_dict

    def get_item_generate_response(self, item_name_or_uuid, vault=None, decode="utf-8"):
        get_item_argv: _OPArgv = self._get_item_argv(
            item_name_or_uuid, vault=vault)
        output = super().get_item(item_name_or_uuid, vault=vault, decode=decode)
        resp_dict = self._generate_response_dict(
            get_item_argv, output, decode=decode)

        return resp_dict

    def get_document(self, document_name_or_uuid: str, vault: str):
        get_doc_argv: _OPArgv = self._get_document_argv(
            document_name_or_uuid, vault=vault)
        output = super().get_document(document_name_or_uuid, vault=vault)
        resp_dict = self._generate_response_dict(get_doc_argv, output)

        return resp_dict
