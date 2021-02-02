from mock_cli.responses import CommandInvocation

from ._py_op_commands import _OPCommandInterface
from ._py_op_cli import _OPArgv

class OPResponseGenerator(_OPCommandInterface):

    def _generate_response_dict(self, argv_obj: _OPArgv,
                                query_name,
                                stdout,
                                stderr,
                                returncode,
                                stdout_encoding,
                                stderr_encoding):
        query_args = argv_obj.query_args()
        query_response = CommandInvocation(query_args, stdout, stderr, returncode, query_name,
                                           stdout_encoding=stdout_encoding, stderr_encoding=stderr_encoding)

        return query_response

    def get_item_generate_response(self, item_name_or_uuid, query_name, vault=None, fields=None, decode="utf-8"):
        out_encoding = err_encoding = decode
        get_item_argv: _OPArgv = self._get_item_argv(
            item_name_or_uuid, vault=vault, fields=fields)
        stdout, stderr, returncode = self._run_raw(get_item_argv, capture_stdout=True, ignore_error=True)
        stdout = stdout.decode(decode)
        stderr = stderr.decode(decode)
        resp_dict = self._generate_response_dict(
            get_item_argv, query_name, stdout, stderr, returncode, out_encoding, err_encoding)

        return resp_dict

    def get_document_generate_response(self, document_name_or_uuid: str, query_name, vault: str = None):
        out_encoding = "binary"
        err_encoding = "utf-8"
        get_doc_argv: _OPArgv = self._get_document_argv(
            document_name_or_uuid, vault=vault)
        stdout, stderr, returncode = self._run_raw(
            get_doc_argv, capture_stdout=True, ignore_error=True)
        stderr = stderr.decode(err_encoding)
        resp_dict = self._generate_response_dict(
            get_doc_argv, query_name, stdout, stderr, returncode, out_encoding, err_encoding)

        return resp_dict
