import json
from json import JSONDecodeError
from os import environ as env
from ._py_op_items import (
    OPItemFactory,
    OPAbstractItem,
    OPLoginItem,
)

from ._py_op_commands import _OPCommandInterface
from ._py_op_deprecation import deprecated
from .py_op_exceptions import (
    OPGetItemException,
    OPGetDocumentException,
    OPInvalidDocumentException,
    OPCmdFailedException,
    OPSignoutException,
    OPForgetException,
    OPGetUserException,
    OPGetVaultException,
    OPGetGroupException,
    OPListEventsException
)


class OP(_OPCommandInterface):
    """
    Class for logging into and querying a 1Password account via the 'op' cli command.
    """

    def __init__(self, vault=None, account_shorthand=None, signin_address=None, email_address=None,
                 secret_key=None, password=None, logger=None, op_path='op'):
        """
        Create an OP object. The 1Password sign-in happens during object instantiation.
        If 'password' is not provided, the 'op' command will prompt on the console for a password.

        If all components of a 1Password account are provided, an initial sign-in is performed,
        otherwise, a normal sign-in is performed. See `op --help` for further explanation.

        Arguments:
            - 'vault': If set, this becomes the default argument to the --vault flag
                       for future queries.
            - 'account_shorthand': The shorthand name for the account on this device.
                                   You may choose this during initial signin, otherwise
                                   1Password converts it from your account address.
                                   See 'op signin --help' for more information.
            - 'signin_address': Fully qualified address of the 1Password account.
                                E.g., 'my-account.1password.com'
            - 'email_address': Email of the address for the user of the account
            - 'secret_key': Secret key for the account
            - 'password': The user's master password
            - 'logger': A logging object. If not provided a basic logger is created and used.
            - 'op_path': optional path to the `op` command, if it's not at the default location

        Raises:
            - OPSigninException if 1Password sign-in fails for any reason.
            - OPNotFoundException if the 1Password command can't be found.
        """
        super().__init__(vault=vault,
                         account_shorthand=account_shorthand,
                         signin_address=signin_address,
                         email_address=email_address,
                         secret_key=secret_key,
                         password=password,
                         logger=logger,
                         op_path=op_path)

    def _get_abstract(self, abstract_obj_type: str, abs_name_or_uuid: str, exception_on_err: OPCmdFailedException):
        lookup_argv = [self.op_path, "get",
                       abstract_obj_type, abs_name_or_uuid]

        try:
            output = self._run(
                lookup_argv, capture_stdout=True, decode="utf-8")
        except OPCmdFailedException as ocfe:
            raise exception_on_err.from_opexception(ocfe) from ocfe

        try:
            item_dict = json.loads(output)
        except JSONDecodeError as jdce:
            raise exception_on_err.from_opexception(jdce) from jdce

        return item_dict

    def get_item(self, item_name_or_uuid, vault=None):
        try:
            output = super().get_item(item_name_or_uuid, vault=vault, decode="utf-8")
        except OPCmdFailedException as ocfe:
            raise OPGetItemException.from_opexception(ocfe) from ocfe

        item_dict = json.loads(output)
        op_item = OPItemFactory.op_item_from_item_dict(item_dict)
        return op_item

    def get_user(self, user_name_or_uuid: str):
        return self._get_abstract('user', user_name_or_uuid, OPGetUserException)

    def get_vault(self, vault_name_or_uuid: str):
        return self._get_abstract('vault', vault_name_or_uuid, OPGetVaultException)

    def get_group(self, group_name_or_uuid: str):
        return self._get_abstract('group', group_name_or_uuid, OPGetGroupException)

    def list_events(self, eventid=None, older=False):
        """
        Returns the 100 most recent events by default.
        The Activity Log is only available for 1Password Business accounts.

        :param eventid: start listing from event with ID eid
        :param older: list events from before the specified event
        :return: Raw JSON list of events
        """
        event_argv = []
        if eventid:
            event_argv = ["--eventid", eventid]
            if older:
                event_argv = ["--older", "--eventid", eventid]

        lookup_argv = [self.op_path, "list", "events"]
        if event_argv:
            lookup_argv.extend(event_argv)

        try:
            output = self._run(
                lookup_argv, capture_stdout=True, decode="utf-8")
        except OPCmdFailedException as ocfe:
            raise OPListEventsException.from_opexception(ocfe) from ocfe

        item_dict = json.loads(output)
        return item_dict

    def get_item_password(self, item_name_or_uuid, vault=None):
        item: OPLoginItem
        item = self.get_item(item_name_or_uuid, vault=vault)
        password = item.password
        return password

    def get_item_filename(self, item_name_or_uuid, vault=None):
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
        item = self.get_item(item_name_or_uuid, vault=vault)
        # Will raise AttributeError if item isn't a OPDocumentItem
        file_name = item.file_name

        return file_name

    def get_document(self, document_name_or_uuid, vault=None):
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
            file_name = self.get_item_filename(
                document_name_or_uuid, vault=vault)
        except AttributeError as ae:
            raise OPInvalidDocumentException(
                "Item has no 'fileName' attribute") from ae

        try:
            document_bytes = super().get_document(document_name_or_uuid, vault=vault)
        except OPCmdFailedException as ocfe:
            raise OPGetDocumentException.from_opexception(ocfe) from ocfe

        return (file_name, document_bytes)

    def signout(self, forget=False):
        account = self.account_shorthand
        token = self.token
        global_flags = ["--session", token, "--account", account]
        signout_argv = [self.op_path, "signout"]
        if forget:
            signout_argv.append("--forget")
        signout_argv.extend(global_flags)
        try:
            self._run(signout_argv)
        except OPCmdFailedException as ocfe:
            raise OPSignoutException.from_opexception(ocfe) from ocfe
        self._sanitize()

    @classmethod
    def forget(cls, account, op_path=None):
        if op_path is None:
            op_path = cls.OP_PATH
        forget_argv = [op_path, "forget", account]
        try:
            cls._run(forget_argv)
        except OPCmdFailedException as ocfe:
            raise OPForgetException.from_opexception(ocfe) from ocfe

    def _sanitize(self):
        self.token = None
        sess_var_name = 'OP_SESSION_{}'.format(self.account_shorthand)
        try:
            env.pop(sess_var_name)
        except KeyError:
            pass

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
        output = super().get_document(item_name_or_uuid)

        return output
