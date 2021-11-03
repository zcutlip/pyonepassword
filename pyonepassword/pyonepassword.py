import json
from json import JSONDecodeError
from os import environ as env
from typing import Dict

from .op_items._op_items_base import OPAbstractItem, OPItemCreateResult
from .op_items._op_item_type_registry import OPItemFactory
from .op_items.login import OPLoginItem, OPLoginItemTemplate
from ._py_op_commands import _OPCommandInterface
from ._py_op_deprecation import deprecated
from .py_op_exceptions import (
    OPGetItemException,
    OPGetDocumentException,
    OPInvalidDocumentException,
    OPCmdFailedException,
    OPSignoutException,
    OPForgetException,
    OPGetCreatedItemException,
    OPGetUserException,
    OPGetVaultException,
    OPGetGroupException,
    OPListEventsException
)


class _OPPrivate(_OPCommandInterface):
    """
    Note: This private class serves to allow an API split and deprecation of initial sign-in support.
    Two separate classes extend this class:
    - 'OP' which no longer supports initial sign-in
    - 'OP_' to which initial-signin API has been moved for deprecation

    Once initial sign-in support has been completely removed, the 'OP' class and this class will be re-consolidated
    """

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

    def get_item(self, item_name_or_uuid, vault=None) -> OPAbstractItem:
        """
        Get an 'item' object from a 1Password vault by name or UUID.
        The returned object may be any of the item types extending OPAbstractItem.
        These currently include:
        - OPLoginItem (template id 1)
        - OPCreditCardItem (template id 2)
        - OPSecureNoteItem (template id 3)
        - OPPasswordItem (template id 5)
        - OPDocumentItem (template id 6)
        - OPServerItem (template id 110)

        Note that getting a document item is not the same as getting the document itself. The
        item only contains metadata about the document such as filename.

        Parameters
        ----------
        item_name_or_uuid: str
            Name or UUID of the item to look up
        vault: str, optional
            The name of a vault to override the object's default vault

        Raises
        ------
        OPGetItemException
            If the lookup fails for any reason.
        OPNotFoundException
            If the 1Password command can't be found.

        Returns
        -------
        item: OPAbstractItem
            An item object of one of the types listed above
        """
        try:
            output = super().get_item(item_name_or_uuid, vault=vault, decode="utf-8")
        except OPCmdFailedException as ocfe:
            raise OPGetItemException.from_opexception(ocfe) from ocfe

        item_dict = json.loads(output)
        op_item = OPItemFactory.op_item_from_item_dict(item_dict)
        return op_item

    def get_user(self, user_name_or_uuid: str) -> Dict:
        return self._get_abstract('user', user_name_or_uuid, OPGetUserException)

    def get_vault(self, vault_name_or_uuid: str):
        return self._get_abstract('vault', vault_name_or_uuid, OPGetVaultException)

    def get_group(self, group_name_or_uuid: str):
        return self._get_abstract('group', group_name_or_uuid, OPGetGroupException)

    def list_events(self, eventid=None, older=False):
        """
        Returns the 100 most recent events by default.
        The Activity Log is only available for 1Password Business accounts.

        Parameters
        ----------
        eventid: str, optional
            start listing from event with ID eid

        older: bool, optional
            list events from before the specified event

        Raises
        ------
        OPListEventsException
            If the lookup fails for any reason.
        OPNotFoundException
            If the 1Password command can't be found.

        Returns
        -------
        str
            Raw JSON list of events
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

    def get_item_password(self, item_name_or_uuid, vault=None) -> str:
        """
        Get the value of the password field from the item specified by name or UUID.

        Parameters
        ----------
        item_name_or_uuid: str
            The item to look up
        vault: str, optional
            The name of a vault to override the object's default vault

        Raises
        ------
        AttributeError
            If the item doesn't have a 'fileName' attribute.
        OPGetItemException
            If the lookup fails for any reason.
        OPNotFoundException
            If the 1Password command can't be found.

        Returns
        -------
        password: str
            Value of the item's 'password' attribute
        """
        item: OPLoginItem
        item = self.get_item(item_name_or_uuid, vault=vault)
        password = item.password
        return password

    def get_item_filename(self, item_name_or_uuid, vault=None):
        """
        Get the fileName attribute a document item from a 1Password vault by name or UUID.

        Parameters
        ----------
        item_name_or_uuid : str
            The item to look up
        vault: str, optional
            The name of a vault to override the object's default vault

        Raises
        ------
        AttributeError
            If the item doesn't have a 'fileName' attribute
        OPGetItemException
            If the lookup fails for any reason
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        file_name: str
            Value of the item's 'fileName' attribute
        """
        item = self.get_item(item_name_or_uuid, vault=vault)
        # Will raise AttributeError if item isn't a OPDocumentItem
        file_name = item.file_name

        return file_name

    def get_document(self, document_name_or_uuid, vault=None):
        """
        Download a document object from a 1Password vault by name or UUID.

        Parameters
        ----------
        item_name_or_uuid : str
            The item to look up
        vault: str, optional
            The name of a vault to override the object's default vault

        Raises
        ------
        OPInvalidDocumentException
            If the retrieved item isn't a document object or lacks a documents expected attributes
        OPGetDocumentException
            If the lookup fails for any reason
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        file_name, document bytes: Tuple[str, bytes]
            A tuple consisting of the filename and bytes of the specified document
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

    def create_item(self, item: OPAbstractItem, item_name: str, vault: str = None) -> OPAbstractItem:
        """
        Create an item entry from the provided item object

        Note: 'item' must be an instance of a type that inherits
        'OPItemTemplateMixin'. Currently this includes:
        - OPLoginItemTemplate

        Parameters
        ----------
        item : OPAbstractItem|OPItemTemplateMixin
            The item template object to create an entry from
        item_name : str
            The user-visible name of the entry to be created. The new entry can later be queried by this name
        vault : str, optional
            The name of a vault to override the OP object's default vault

        Raises
        ------
        OPCreateItemNotSupportedException
            If the 'item' object does not support item creation
        OPCreateItemException
            If item creation fails for any reason during execution
        OPNotFoundException
            If the 1Password command can't be found
        OPGetCreatedItemException
            If item creation succeeds, but fetching the item fails for some reason
            Exception object's UUID attribute contains the created items's UUID

        Returns
        -------
        created_item : OPAbstractItem
            The item object fetched after creating a new item from template
        """
        result_str = super().create_item(item, item_name, vault=vault)
        result = json.loads(result_str)
        result = OPItemCreateResult(result)
        try:
            created_item = self.get_item(result.uuid, vault=result.vault_uuid)
        except OPGetItemException as e:
            msg = f"Failed to get newly created item: [{e}], Item UUID: {result.uuid}"
            raise OPGetCreatedItemException(msg, result.uuid) from e
        return created_item

    def create_login_item(self, item_name: str, username: str, password: str, url=None, vault=None):
        new_item = OPLoginItemTemplate(username, password, url=url)
        created_item = self.create_item(
            new_item, item_name, vault=vault)
        return created_item

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
        self._token = None
        sess_var_name = 'OP_SESSION_{}'.format(self.account_shorthand)
        try:
            env.pop(sess_var_name)
        except KeyError:
            pass


class OP(_OPPrivate):
    """
    Class for logging into and querying a 1Password account via the 'op' cli command.
    """

    def __init__(self,
                 vault=None,
                 account_shorthand=None,
                 password=None,
                 logger=None,
                 op_path='op',
                 use_existing_session=False,
                 password_prompt=True):
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
            - 'password': The user's master password
            - 'logger': A logging object. If not provided a basic logger is created and used.
            - 'op_path': optional path to the `op` command, if it's not at the default location
            - 'use_existing_session': A boolean indicating whether an existing login session should be used if possible
            - 'password_prompt': A boolean indicating whether an interactive password prompt on the console should be presented if necessary

        Raises:
            - OPSigninException if 1Password sign-in fails for any reason.
            - OPNotSignedInException if:
                - No session is available for reuse (or session reuse not requested), and
                - no password provided, and
                - interactive password prompt is supressed
            - OPNotFoundException if the 1Password command can't be found.
        """
        super().__init__(vault=vault,
                         account_shorthand=account_shorthand,
                         password=password,
                         logger=logger,
                         op_path=op_path,
                         use_existing_session=use_existing_session,
                         password_prompt=password_prompt)


@deprecated("OP with initial sign-in is deprecated and will soon be removed")
class OP_(_OPPrivate):
    """
    Class for logging into and querying a 1Password account via the 'op' cli command.

    Note: This class, which supports additional parameters for initial sign-in is deprecated and will soon be removed.
    """

    def __init__(self,
                 vault=None,
                 account_shorthand=None,
                 signin_address=None,
                 email_address=None,
                 secret_key=None,
                 password=None,
                 logger=None,
                 op_path='op',
                 use_existing_session=False,
                 password_prompt=True):
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
            - 'use_existing_session': A boolean indicating whether an existing login session should be used if possible
            - 'password_prompt': A boolean indicating whether an interactive password prompt on the console should be presented if necessary

        Raises:
            - OPSigninException if 1Password sign-in fails for any reason.
            - OPNotSignedInException if:
                - No session is available for reuse (or session reuse not requested), and
                - no password provided, and
                - interactive password prompt is supressed
            - OPNotFoundException if the 1Password command can't be found.
        """
        super().__init__(vault=vault,
                         account_shorthand=account_shorthand,
                         signin_address=signin_address,
                         email_address=email_address,
                         secret_key=secret_key,
                         password=password,
                         logger=logger,
                         op_path=op_path,
                         use_existing_session=use_existing_session,
                         password_prompt=password_prompt)
