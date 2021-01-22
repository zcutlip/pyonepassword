import os
from pathlib import Path
from ._py_op_commands import _OPCommandInterface
from ._py_op_cli import _OPArgv


class OPQueryResponse:
    def __init__(self, query_dict, output, error_output, returncode, stdout_encoding="utf-8", stderr_encoding="utf-8"):
        self.query_dict = query_dict
        self.stdout_encoding = stdout_encoding
        self.output = output
        self.stderr_encoding = stderr_encoding
        self.error_output = error_output
        self.returncode = returncode

    def record_response(self, response_dir, response_name):
        resp_path: Path
        if isinstance(response_name, str):
            response_name = Path(response_name)

        resp_path = Path(response_dir, response_name)

        resp_path.mkdir(parents=True, exist_ok=True)
        # TODO: stderr binary output doesn't really make sense
        # should we check for it and raise an exception?
        if self.stdout_encoding == "binary":
            binary = True
            output_ext = "bin"
        else:
            binary = False
            output_ext = "txt"

        output_path = Path(resp_path, f"output.{output_ext}")
        error_output_path = Path(resp_path, "error_output.txt")

        error_output_path.write_text(self.error_output)
        if binary:
            output_path.write_bytes(self.output)
        else:
            output_path.write_text(self.output)
        response_dict = {
            "query": self.query_dict,
            "response": {
                "stdout_encoding": self.stdout_encoding,
                "stderr_encoding": self.stderr_encoding,
                "exit_status": self.returncode,
                "response_name": str(response_name),
                "stdout": os.path.basename(output_path),
                "stderr": os.path.basename(error_output_path)
            }
        }

        return response_dict


class OPQueryDict(dict):
    def __init__(self, response_dir):
        _dict = {
            "response_dir": response_dir,
            "queries": []}
        super().__init__(_dict)

    def add_query(self, query: OPQueryResponse, query_name: str):
        response_dict = query.record_response(self.response_dir, query_name)
        self.queries.append(response_dict)

    @property
    def queries(self):
        return self["queries"]

    @property
    def response_dir(self):
        return self["response_dir"]

class OPResponseGenerator(_OPCommandInterface):

    def _generate_response_dict(self, argv_obj: _OPArgv, stdout, stderr, returncode, stdout_encoding, stderr_encoding):
        query_dict = argv_obj.query_dict()
        query_response = OPQueryResponse(
            query_dict, stdout, stderr, returncode, stdout_encoding=stdout_encoding, stderr_encoding=stderr_encoding)

        return query_response

    def get_item_generate_response(self, item_name_or_uuid, vault=None, fields=None, decode="utf-8"):
        out_encoding = err_encoding = decode
        get_item_argv: _OPArgv = self._get_item_argv(
            item_name_or_uuid, vault=vault, fields=fields)
        stdout, stderr, returncode = self._run_raw(get_item_argv, capture_stdout=True, ignore_error=True)
        stdout = stdout.decode(decode)
        stderr = stderr.decode(decode)
        resp_dict = self._generate_response_dict(get_item_argv, stdout, stderr, returncode, out_encoding, err_encoding)

        return resp_dict

    def get_document_generate_response(self, document_name_or_uuid: str, vault: str = None):
        out_encoding = "binary"
        err_encoding = "utf-8"
        get_doc_argv: _OPArgv = self._get_document_argv(
            document_name_or_uuid, vault=vault)
        stdout, stderr, returncode = self._run_raw(
            get_doc_argv, capture_stdout=True, ignore_error=True)
        stderr = stderr.decode(err_encoding)
        resp_dict = self._generate_response_dict(
            get_doc_argv, stdout, stderr, returncode, out_encoding, err_encoding)

        return resp_dict
