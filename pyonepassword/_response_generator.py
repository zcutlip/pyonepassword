from pathlib import Path
from ._py_op_commands import _OPCommandInterface
from ._py_op_cli import _OPArgv


class OPQueryResponse:
    def __init__(self, query_dict, response_obj, binary=False):
        self.query_dict = query_dict
        self.binary = binary
        self.response = response_obj

    def record_response(self, response_file_path):
        resp_path: Path
        if isinstance(response_file_path, str):
            resp_path = Path(response_file_path)
        else:
            resp_path = response_file_path

        resp_path.parent.mkdir(parents=True, exist_ok=True)
        if self.binary:
            resp_path.write_bytes(self.response)
        else:
            resp_path.write_text(self.response)
        response_dict = {
            "query": self.query_dict,
            "response": {
                "binary": self.binary,
                "response-file": str(resp_path)
            }
        }

        return response_dict


class OPResponseGenerator(_OPCommandInterface):

    def _generate_response_dict(self, argv_obj, output, decode=None):
        if decode:
            binary = False
        else:
            binary = True
        query_dict = argv_obj.query_dict()
        query_response = OPQueryResponse(query_dict, output, binary=binary)

        return query_response

    def get_item_generate_response(self, item_name_or_uuid, vault=None, fields=None, decode="utf-8"):
        get_item_argv: _OPArgv = self._get_item_argv(
            item_name_or_uuid, vault=vault, fields=fields)
        output = super().get_item(item_name_or_uuid, vault=vault, fields=fields, decode=decode)
        resp_dict = self._generate_response_dict(
            get_item_argv, output, decode=decode)

        return resp_dict

    def get_document_generate_response(self, document_name_or_uuid: str, vault: str = None):
        get_doc_argv: _OPArgv = self._get_document_argv(
            document_name_or_uuid, vault=vault)
        output = super().get_document(document_name_or_uuid, vault=vault)
        resp_dict = self._generate_response_dict(get_doc_argv, output)

        return resp_dict
