import os
from pathlib import Path
from ._py_op_commands import _OPCommandInterface
from ._py_op_cli import _OPArgv


class OPQueryResponse:
    def __init__(self, query_dict, output, error_output, returncode, encoding="utf-8"):
        self.query_dict = query_dict
        self.encoding = encoding
        self.output = output
        self.error_output = error_output
        self.returncode = returncode

    def record_response(self, response_dir):
        resp_path: Path
        if isinstance(response_dir, str):
            resp_path = Path(response_dir)
        else:
            resp_path = response_dir

        resp_path.mkdir(parents=True, exist_ok=True)
        if self.encoding == "binary":
            binary = True
            output_ext = ".bin"
        else:
            binary = False
            output_ext = ".txt"

        output_path = Path(resp_path, f"output.{output_ext}")
        error_output_path = Path(resp_path, f"error_output.{output_ext}")

        if binary:
            output_path.write_bytes(self.output)
            error_output_path.write_bytes(self.error_output)
        else:
            output_path.write_text(self.output)
            error_output_path.write_text(self.error_output)
        response_dict = {
            "query": self.query_dict,
            "response": {
                "encoding": self.encoding,
                "response_dir": os.path.basename(resp_path),
                "stdout": os.path.basename(output_path),
                "stderr": os.path.basename(error_output_path)
            }
        }

        return response_dict


class OPResponseGenerator(_OPCommandInterface):

    def _generate_response_dict(self, argv_obj: _OPArgv, stdout, stderr, returncode, decode=None):
        if decode:
            binary = False
        else:
            binary = True
        query_dict = argv_obj.query_dict()
        query_response = OPQueryResponse(
            query_dict, stdout, stderr, returncode, binary=binary)

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
        stdout, stderr, returncode = self._run_raw(
            get_doc_argv, capture_stdout=True, ignore_error=True)
        resp_dict = self._generate_response_dict(
            get_doc_argv, stdout, stderr, returncode)

        return resp_dict
