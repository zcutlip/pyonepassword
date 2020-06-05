import subprocess
import json
import logging
from abc import ABCMeta, abstractmethod
from os import environ as env
from ._py_op_items import (
    OPItemFactory,
    OPAbstractItem,
    OPLoginItem,
)
from ._py_op_deprecation import deprecated


class _OPAbstractException(Exception, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, stderr_out, returncode, msg):
        super().__init__(msg)
        self.err_output = stderr_out
        self.returncode = returncode


class OPSigninException(_OPAbstractException):
    MSG = "1Password sign-in failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode, self.MSG)


# Keep this exception class around for a bit
# so any code handling this exception instead of OPGetItemException
# can still work
@deprecated("handle OPGetItemException instead")
class OPLookupException(_OPAbstractException):
    MSG = "1Password lookup failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode, self.MSG)


# For now have this class extend OPLookupException
# so code can handle that exception or this one
# TODO: remove OPLookupException, have this class extend
# _OPAbstractException
class OPGetItemException(OPLookupException):
    MSG = "1Password 'get item' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode, self.MSG)


class OPGetDocumentException(_OPAbstractException):
    MSG = "1Password 'get document' failed."

    def __init__(self, stderr_out, returncode):
        super().__init__(stderr_out, returncode, self.MSG)


class OPInvalidDocumentException(OPGetDocumentException):

    def __init__(self, msg):
        msg = "{}: {}".format(self.MSG, msg)
        super().__init__("", 0, msg)


class OPNotFoundException(Exception):
    MSG = "1Password cli command not found at path: %s"

    def __init__(self, op_path, errno):
        msg = self.MSG % op_path
        self.errno = errno
        super().__init__(msg)


class OP:
    """
    Class for logging into and querying a 1Password account via the 'op' cli command.
    """

    def __init__(self, account_shorthand, signin_address=None, email_address=None,
                 secret_key=None, password=None, logger=None, op_path='op'):
        """
        Create an OP object. The 1Password sign-in happens during object instantiation.
        If 'password' is not provided, the 'op' command will prompt on the console for a password.

        If all components of a 1Password account are provided, an initial sign-in is performed,
        otherwise, a normal sign-in is performed. See `op --help` for further explanation.

        Arguments:
            - 'op_path': optional path to the `op` command, if it's not at the default location
            - 'signin_address': Fully qualified address of the 1Password account.
                                E.g., 'my-account.1password.com'
            - 'email_address': Email of the address for the user of the account
            - 'secret_key': Secret key for the account
            - 'password': The user's master password
            - 'logger': A logging object. If not provided a basic logger is created and used.

        Raises:
            - OPSigninException if 1Password sign-in fails for any reason.
            - OPNotFoundException if the 1Password command can't be found.
        """
        self.account_shorthand = account_shorthand
        self.op_path = op_path
        if not logger:
            logging.basicConfig(format="%(message)s", level=logging.DEBUG)
            logger = logging.getLogger()

        self.logger = logger
        initial_signin_args = [account_shorthand,
                               signin_address,
                               email_address,
                               secret_key,
                               password]
        initial_signin = (None not in initial_signin_args)

        if initial_signin:
            self.token = self._do_initial_signin(*initial_signin_args)
            # export OP_SESSION_<signin_address>
        else:
            self.token = self._do_normal_signin(password)
        sess_var_name = 'OP_SESSION_{}'.format(self.account_shorthand)
        # TODO: return alread-decoded token from sign-in
        env[sess_var_name] = self.token.decode()

    def _do_normal_signin(self, password):
        self.logger.info("Doing normal (non-initial) 1Password sign-in")
        signin_argv = [self.op_path, "signin", "--output=raw"]
        print("")
        token = self._run_signin(signin_argv, password=password).rstrip()
        return token

    def _do_initial_signin(self, account_shorthand, signin_address, email_address, secret_key, password):
        self.logger.info(
            "Performing initial 1Password sign-in to {} as {}".format(signin_address, email_address))
        signin_argv = [self.op_path, "signin", signin_address,
                       email_address, secret_key, "--output=raw"]
        print("")
        token = self._run_signin(signin_argv, password=password).rstrip()

        return token

    def _run_signin(self, argv, password=None):
        return self._run(argv, OPSigninException, capture_stdout=True, input_string=password)

    def _run_get_item(self, argv, input_string=None, decode=None):
        return self._run(argv, OPLookupException, capture_stdout=True, input_string=input_string, decode=decode)

    def _run_get_document(self, argv, input_string=None, decode=None):
        return self._run(argv, OPGetDocumentException, capture_stdout=True, input_string=input_string, decode=decode)

    def _run(self, argv, op_exception_class, capture_stdout=False, input_string=None, decode=None):
        _ran = None
        stdout = subprocess.PIPE if capture_stdout else None
        if input_string:
            if isinstance(input_string, str):
                input_string = input_string.encode("utf-8")
        try:
            _ran = subprocess.run(argv, input=input_string,
                                  stderr=subprocess.PIPE, stdout=stdout, env=env)
        except FileNotFoundError as err:
            self.logger.error(
                "1Password 'op' command not found at: {}".format(argv[0]))
            self.logger.error(
                "See https://support.1password.com/command-line-getting-started/ for more information,")
            self.logger.error(
                "or install from Homebrew with: 'brew install 1password-cli")
            raise OPNotFoundException(argv[0], err.errno) from err

        output = None
        try:
            _ran.check_returncode()
            if capture_stdout:
                output = _ran.stdout.decode(decode) if decode else _ran.stdout
        except subprocess.CalledProcessError as err:
            stderr_output = _ran.stderr.decode("utf-8").rstrip()
            returncode = _ran.returncode
            raise op_exception_class(stderr_output, returncode) from err

        return output

    def get_item(self, item_name_or_uuid):
        lookup_argv = [self.op_path, "get", "item", item_name_or_uuid]
        output = self._run_get_item(lookup_argv, decode="utf-8")
        item_dict = json.loads(output)
        op_item = OPItemFactory.op_item_from_item_dict(item_dict)
        return op_item

    def get_item_password(self, item_name_or_uuid):
        item: OPLoginItem
        item = self.get_item(item_name_or_uuid)
        password = item.password
        return password

    def get_item_filename(self, item_name_or_uuid):
        """
        Get the fileName attribute a document item from a 1Password vault by name or UUID.

        Arguments:
            - 'item_name_or_uuid': The item to look up
        Raises:
            - AttributeError if the item doesn't have a 'fileName' attribute.
            - OPGetItemException if the lookup fails for any reason.
            - OPNotFoundException if the 1Password command can't be found.
        Returns:
            - value of the item's 'fileName' attribute
        """
        item = self.get_item(item_name_or_uuid)
        # Will raise AttributeError if item isn't a OPDocumentItem
        file_name = item.file_name

        return file_name

    def get_document(self, document_name_or_uuid):
        """
        Download a document object from a 1Password vault by name or UUID.

        Arguments:
            - 'item_name_or_uuid': The item to look up
        Raises:
            - OPInvalidDocumentException if the retrieved item isn't a document
              object or lacks a documents expected attributes.
            - OPGetDocumentException if the lookup fails for any reason.
            - OPNotFoundException if the 1Password command can't be found.
        Returns:
            - Tuple: (filename string, bytes of the specified document)
        """
        try:
            file_name = self.get_item_filename(document_name_or_uuid)
        except AttributeError as ae:
            raise OPInvalidDocumentException(
                "Item has no 'fileName' attribute") from ae
        get_document_argv = [self.op_path,
                             "get", "document", document_name_or_uuid]
        document_bytes = self._run_get_document(get_document_argv)

        return (file_name, document_bytes)

    @deprecated("use get_item() or get_item_password()")
    def lookup(self, item_name_or_uuid, field_designation="password"):
        """
        Look up an item in a 1Password vault by name or UUID.

        Arguments:
            - 'item_name_or_uuid': The item to look up
            - 'field_designation': The name of the field for which a value will be returned
        Raises:
            - OPGetItemException if the lookup fails for any reason.
            - OPNotFoundException if the 1Password command can't be found.
        Returns:
            - Value of the specified field to lookup
        """
        # lookup_argv = [self.op_path, "get", "item", item_name_or_uuid]
        # output = self._run_lookup(lookup_argv, self.token, decode="utf-8")
        # item = json.loads(output)
        # details = item['details']
        # fields = details['fields']
        # value = None
        # for field in fields:
        #     if 'designation' not in field.keys():
        #         continue
        #     if field['designation'] == field_designation:
        #         value = field['value']
        item: OPAbstractItem
        if field_designation == "password":
            value = self.get_item_password(item_name_or_uuid)
        else:
            item = self.get_item(item_name_or_uuid)
            value = item.get_item_field_value(field_designation)
        return value

    @deprecated("use get_document()")
    def download(self, item_name_or_uuid):
        """
        Download a document object from a 1Password vault by name or UUID.

        Arguments:
            - 'item_name_or_uuid': The item to look up
        Raises:
            - OPGetDocumentException if the lookup fails for any reason.
            - OPNotFoundException if the 1Password command can't be found.
        Returns:
            - Bytes of the specified document
        """
        lookup_argv = [self.op_path, "get", "document", item_name_or_uuid]
        output = self._run_get_document(lookup_argv)

        return output
