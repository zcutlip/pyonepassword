import subprocess
import json
import logging


class OPSigninException(Exception):
    MSG = "1Password sign-in failed."

    def __init__(self, msg, stderr_out, returncode):
        super().__init__(msg)
        self.err_output = stderr_out
        self.returncode = returncode


class OPLookupException(OPSigninException):
    MSG = "1Password lookup failed."


class OP:
    OP_PATH = "/usr/local/bin/op"

    def __init__(self, op_path=OP_PATH, signin_address=None, email_address=None,
                 secret_key=None, password=None, logger=None):
        self.op_path = op_path
        if not logger:
            logging.basicConfig(format="%(message)s", level=logging.DEBUG)
            logger = logging.getLogger()

        self.logger = logger
        initial_signin_args = [signin_address, email_address, secret_key, password]
        initial_signin = (None not in initial_signin_args)

        if initial_signin:
            self.token = self._do_initial_signin(*initial_signin_args)
        else:
            self.token = self._do_normal_signin(password)

    def _do_normal_signin(self, password):
        self.logger.info("Doing normal (non-initial) 1Password sign-in")
        signin_argv = [self.op_path, "signin", "--output=raw"]
        print("")
        token = self._run_signin(signin_argv, password=password).rstrip()
        return token

    def _do_initial_signin(self, signin_address, email_address, secret_key, password):
        self.logger.info("Performing initial 1Password sign-in to {} as {}".format(signin_address, email_address))
        signin_argv = [self.op_path, "signin", signin_address, email_address, secret_key, "--output=raw"]
        print("")
        token = self._run_signin(signin_argv, password=password).rstrip()

        return token

    def _run_signin(self, argv, password=None):
        return self._run(argv, OPSigninException, capture_stdout=True, input_string=password)

    def _run_lookup(self, argv, input_string, decode=None):
        return self._run(argv, OPLookupException, capture_stdout=True, input_string=input_string, decode=None)

    def _run(self, argv, op_exception_class, capture_stdout=False, input_string=None, decode=None):
        _ran = None
        stdout = subprocess.PIPE if capture_stdout else None
        if input_string:
            if isinstance(input_string, str):
                input_string = input_string.encode("utf-8")
            _ran = subprocess.run(argv, input=input_string, stderr=subprocess.PIPE, stdout=stdout)
        else:
            _ran = subprocess.run(argv, stderr=subprocess.PIPE, stdout=stdout)

        output = None
        try:
            _ran.check_returncode()
            if capture_stdout:
                output = _ran.stdout.decode(decode) if decode else _ran.stdout
        except subprocess.CalledProcessError:
            stderr_output = _ran.stderr.rstrip()
            returncode = _ran.returncode
            msg = op_exception_class.MSG
            raise op_exception_class(msg, stderr_output, returncode)

        return output

    def lookup(self, item_name_or_uuid, field_designation="password"):
        lookup_argv = [self.op_path, "get", "item", item_name_or_uuid]
        output = self._run_lookup(lookup_argv, self.token, decode="utf-8")
        item = json.loads(output)
        details = item['details']
        fields = details['fields']
        value = None
        for field in fields:
            if field['designation'] == field_designation:
                value = field['value']

        return value
