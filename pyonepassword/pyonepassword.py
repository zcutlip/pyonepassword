import logging
from os import environ as env
from typing import Optional, Union

from ._py_op_commands import (
    EXISTING_AUTH_IGNORE,
    ExistingAuthEnum,
    _OPCommandInterface
)
from ._py_op_deprecation import deprecated_kwargs
from .account import OPAccountList
from .op_items._item_list import OPItemList
from .op_items._new_item import OPNewItemMixin
from .op_items._op_item_type_registry import OPItemFactory
from .op_items._op_items_base import OPAbstractItem
from .op_items.generic_item import _OPGenericItem
from .op_items.login import OPLoginItemNewPrimaryURL, OPLoginItemTemplate
from .op_items.password_recipe import OPPasswordRecipe
from .op_items.totp import OPTOTPItem
from .op_objects import (
    OPGroup,
    OPGroupDescriptorList,
    OPUser,
    OPUserDescriptorList,
    OPVault,
    OPVaultDescriptorList
)
from .py_op_exceptions import (
    OPCmdFailedException,
    OPDocumentDeleteException,
    OPDocumentGetException,
    OPForgetException,
    OPInvalidDocumentException,
    OPInvalidItemException,
    OPItemDeleteException,
    OPItemGetException,
    OPSignoutException
)
from .version import PyOPAboutMixin


class OP(_OPCommandInterface, PyOPAboutMixin):
    """
    Class for logging into and querying a 1Password account via the 'op' cli command.
    """
    @deprecated_kwargs(use_existing_session='existing_auth',
                       account_shorthand='account')
    def __init__(self,
                 account: Optional[str] = None,
                 account_shorthand: Optional[str] = None,
                 password: Optional[str] = None,
                 existing_auth: ExistingAuthEnum = EXISTING_AUTH_IGNORE,
                 use_existing_session: bool = False,
                 password_prompt: bool = True,
                 vault: Optional[str] = None,
                 op_path: str = 'op',
                 logger: Optional[logging.Logger] = None):
        """
        Create an OP object. The 1Password (non-initial) sign-in happens during object instantiation.

        Parameters
        ----------
        account : str, optional
            May be any account identifier accepted by the op --account flag:
            account shorthand, sign-in address, account ID, or user ID
        password : str, optional
            If provided, the password will be piped to the 'op' command over stdin
        existing_auth : ExistingAuthEnum
            Whether existing authentication must be used, used if possible, or ignored
            Valid values:
              - EXISTING_AUTH_AVAIL: Use existing authentication if available
              - EXISTING_AUTH_IGNORE: Reauthenticate, ignoring any existing authentication
              - EXISTING_AUTH_REQD: Use existing authentication, failing if there isn't a valid session available
        password_prompt : bool
            Whether an interactive password prompt on the console should be presented if necessary
        vault : str, optional
            If set, this becomes the default argument to the --vault flag
            for future queries.
        op_path : str, optional
            Optional path to the `op` command, if it's not at the default location
        logger : logging.Logger
            A logging object. If not provided a basic logger is created and used

        Raises
        ------
        OPSigninException
            If 1Password sign-in fails for any reason.
        OPNotSignedInException
            if:
                - No session is available for reuse (or session reuse not requested), and
                - no password provided,
                - interactive password prompt is supressed, and
                - biometric authenticaiotn is disabled
        OPNotFoundException
            If the 1Password command can't be found
        """
        super().__init__(vault=vault,
                         account=account,
                         password=password,
                         logger=logger,
                         op_path=op_path,
                         existing_auth=existing_auth,
                         password_prompt=password_prompt)

    def item_get(self, item_identifier, vault=None, include_archive=False) -> OPAbstractItem:
        """
        Get an 'item' object from a 1Password vault.
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
        item_identifier: str
            Name or ID of the item to look up
        vault: str, optional
            The name or ID of a vault to override the object's default vault

        Note:
            If a non-unique item identifier is provided (e.g., item name/title), and there
            is more than one item that matches, OPItemGetException will be raised. Check the
            error message in OPItemGetException.err_output for details

        Raises
        ------
        OPItemGetException
            If the lookup fails for any reason during command execution
        OPInvalidItemException
            If the item JSON fails to decode
        OPUnknownItemTypeException
            If the item object returned by 1Password isn't a known type
        OPNotFoundException
            If the 1Password command can't be found
        Returns
        -------
        item: OPAbstractItem
            An item object of one of the types listed above
        """

        output = super()._item_get(item_identifier, vault=vault,
                                   decode="utf-8", include_archive=include_archive)
        op_item = OPItemFactory.op_item(output)
        return op_item

    def item_get_totp(self, item_identifier: str, vault=None) -> OPTOTPItem:
        """
        Get a TOTP code from the item specified by name or UUID.

        Note: Items in the Archive are ignored by default. To get the TOTP for an
        item in the Archive, specify the item by UUID.

        Parameters
        ----------
        item_identifier: str
            Name or ID of the item to look up
        vault: str, optional
            The name or ID of a vault to override the object's default vault

        Note:
            If a non-unique item identifier is provided (e.g., item name/title), and there
            is more than one item that matches, OPItemGetException will be raised. Check the
            error message in OPItemGetException.err_output for details

        Raises
        ------
        OPItemGetException
            If the lookup fails for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        totp_code: str
            A string representing the TOTP code
        """
        output = super()._item_get_totp(item_identifier, vault=vault, decode="utf-8")
        # strip newline
        totp = OPTOTPItem(output)
        return totp

    def user_get(self, user_name_or_id: str) -> OPUser:
        """
        Return the details for the user specified by name or UUID.

        Parameters
        ----------
        user_name_or_id: str
            Name or ID of the user to look up
        Raises
        ------
        OPUserGetException
            If the lookup fails for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        user: OPuser
            An object representing the details of the requested user
        """
        user_json = super()._user_get(user_name_or_id)
        user = OPUser(user_json)
        return user

    def user_list(self, group_name_or_id=None, vault_name_or_id=None) -> OPUserDescriptorList:
        """
        Return a list of users in an account.

        Parameters
        ----------
        group_name_or_id: str
            Name or ID of a group to restrict user listing to
        vault_name_or_id: str
            Name or ID of a vault to restrict user listing to

        Raises
        ------
        OPUserListException
            If the user list operation for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        user: OPUserDescriptorList
            An object representing a list of user descriptors
        """
        user_list: Union[str, OPUserDescriptorList]

        user_list = self._user_list(
            group_name_or_id=group_name_or_id, vault=vault_name_or_id)
        user_list = OPUserDescriptorList(user_list)
        return user_list

    def vault_get(self, vault_name_or_id: str) -> OPVault:
        """
        Return the details for the vault specified by name or UUID.

        Parameters
        ----------
        vault_name_or_id: str
            Name or UUID of the vault to look up

        Raises
        ------
        OPVaultGetException
            If the lookup fails for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        vault: OPVault
            An object representing the details of the requested vault
        """
        vault_json = super()._vault_get(vault_name_or_id, decode="utf-8")
        vault = OPVault(vault_json)
        return vault

    def vault_list(self, group_name_or_id=None, user_name_or_id=None) -> OPVaultDescriptorList:
        """
        Return a list of vaults in an account.

        Parameters
        ----------
        group_name_or_id: str
            Name or ID of a group to restrict vault listing to
        user_name_or_id: str
            Name or ID of a user to restrict vault listing to

        Raises
        ------
        OPVaultListException
            If the vault list operation for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        user: OPVaultDescriptorList
            An object representing a list of vault descriptors
        """
        vault_list_json = super()._vault_list(
            group_name_or_id=group_name_or_id, user_name_or_id=user_name_or_id)
        vault_list = OPVaultDescriptorList(vault_list_json)
        return vault_list

    def group_get(self, group_name_or_id: str) -> OPGroup:
        """
        Return the details for the group specified by name or UUID.

        Parameters
        ----------
        group_name_or_id: str
            Name or UUID of the group to look up

        Raises
        ------
        OPGroupGetException
            If the lookup fails for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        user: OPGroup
            An object representing the details of the requested group
        """
        group_json = super()._group_get(group_name_or_id, decode="utf-8")
        group = OPGroup(group_json)
        return group

    def group_list(self, user_name_or_id=None, vault=None) -> OPGroupDescriptorList:
        """
        Return a list of groups in an account.

        Parameters
        ----------
        user_name_or_id: str
            Name or ID of a user to restrict vault listing to
        group_name_or_id: str
            Name or ID of a group to restrict vault listing to

        Raises
        ------
        OPGroupListException
            If the group list operation for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        user: OPGroupDescriptorList
            An object representing a list of vault descriptors
        """
        group_list: Union[str, OPGroupDescriptorList]
        group_list = self._group_list(
            user_name_or_id=user_name_or_id, vault=vault)
        group_list = OPGroupDescriptorList(group_list)
        return group_list

    def item_get_password(self, item_identifier, vault=None) -> str:
        """
        Get the value of the password field from the item specified by name or UUID.

        Parameters
        ----------
        item_identifier: str
            The item to look up
        vault: str, optional
            The name or ID of a vault to override the object's default vault

        Raises
        ------
        AttributeError
            If the item doesn't have a 'fileName' attribute.
        OPItemGetException
            If the lookup fails for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found.

        Returns
        -------
        password: str
            Value of the item's 'password' attribute
        """
        item: OPAbstractItem
        item = self.item_get(item_identifier, vault=vault)

        # satisfy 'mypy': OPAbstractItem has no "password" attribute
        if not hasattr(item, "password"):
            raise OPInvalidItemException(
                f"Item: {item.title} has no password attribute")
        else:
            password = item.password
        return password

    def item_get_filename(self, item_identifier, vault=None, include_archive=False):
        """
        Get the fileName attribute a document item from a 1Password vault by name or UUID.

        Parameters
        ----------
        item_identifier: str
            The item to look up
        vault: str, optional
            The name or ID of a vault to override the object's default vault

        Note:
            If a non-unique item identifier is provided (e.g., item name/title), and there
            is more than one item that matches, OPItemGetException will be raised. Check the
            error message in OPItemGetException.err_output for details

        Raises
        ------
        AttributeError
            If the item doesn't have a 'fileName' attribute
        OPItemGetException
            If the lookup fails for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        file_name: str
            Value of the item's 'fileName' attribute
        """
        item = self.item_get(item_identifier, vault=vault,
                             include_archive=include_archive)

        # raise AttributeError if item isn't a OPDocumentItem
        # we have to raise it ourselves becuase mypy complains OPAbstractItem doesn't have
        # '.file_name'
        if hasattr(item, "file_name"):
            file_name = item.file_name
        else:
            raise AttributeError(
                f"{item.__class__.__name__} object has no attribute 'file_name'")

        return file_name

    def document_get(self, document_name_or_id, vault=None, include_archive=False):
        """
        Download a document object from a 1Password vault by name or UUID.

        Parameters
        ----------
        document_name_or_id : str
            The item to look up
        vault: str, optional
            The name or ID of a vault to override the object's default vault

        Raises
        ------
        OPInvalidDocumentException
            If the retrieved item isn't a document object or lacks a documents expected attributes
        OPDocumentGetException
            If document lookup fails for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        file_name, document bytes: Tuple[str, bytes]
            A tuple consisting of the filename and bytes of the specified document
        """
        try:
            file_name = self.item_get_filename(
                document_name_or_id, vault=vault, include_archive=include_archive)
        except AttributeError as ae:
            raise OPInvalidDocumentException(
                "Item has no 'fileName' attribute") from ae
        except OPCmdFailedException as ocfe:
            raise OPDocumentGetException.from_opexception(ocfe) from ocfe

        try:
            document_bytes = super()._document_get(document_name_or_id,
                                                   vault=vault, include_archive=include_archive)
        except OPCmdFailedException as ocfe:
            raise OPDocumentGetException.from_opexception(ocfe) from ocfe

        return (file_name, document_bytes)

    def document_delete(self, document_identifier: str, vault: Optional[str] = None, archive: bool = False) -> str:
        """
        Delete a document object based on document name or unique identifier

        Parameters
        ----------
        document_identifier : str
            Name or identifier of the document to delete
        vault : str, optional
            The name or ID of a vault to override the default vault, by default None
        archive : bool, optional
            Whether to archive or permanently delete the item, by default False

        Returns
        -------
        document_id: str
            Unique identifier of the item deleted

        Raises
        ------
        OPDocumentDeleteException
            - If the document to be deleted is not found
            - If there is more than one item matching 'document_identifier'
            - If the delete operation fails for any other reason
        """
        try:
            output = super()._item_get(document_identifier, vault=vault)
            item = _OPGenericItem(output)
        except OPItemGetException as e:
            raise OPDocumentDeleteException.from_opexception(e)
        # we want to return the explicit ID even if we were
        # given an document name or other identifier
        # that way the caller knows exactly what got deleted
        # can match it up with what they expected to be deleted, if desired
        document_id = item.unique_id

        # 'op document delete' doesn't have any stdout, so we're not
        # capturing any here
        self._document_delete(document_id, vault=vault, archive=archive)

        return document_id

    def item_list(self, categories=[], include_archive=False, tags=[], vault=None):
        """
        Return a list of items in an account.

        Parameters
        ----------
        categories: List[str], optional
            A list of category names to restrict list to
        include_archive: bool, optional
            Include items in the Archive in the list
        tags: List[str], optional
            A list of tags to restrict list to
        vault: str, optional
            The name or ID of a vault to override the object's default vault

        Raises
        ------
        OPUserListException
            If the user list operation for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        user: OPUserDescriptorList
            An object representing a list of user descriptors
        """
        item_list_json = self._item_list(
            categories, include_archive, tags, vault)
        item_list = OPItemList(item_list_json)
        return item_list

    # TODO: Item creation is hard to test in an automated way since it results in changed
    #   state. There are operations during item creation that expect state to change from
    #   before to after item creation
    #   There is ongoing work in mock-op and mock-cli-framework to simulate changed state
    #   when this is complete these functions need to be tested
    #
    #   For now, ignore testing coverate
    def item_create(self,
                    new_item: OPNewItemMixin,
                    password_recipe: OPPasswordRecipe = None,
                    vault: Optional[str] = None):  # pragma: no coverage
        """
        Create a new item in the authenticated 1Password account

        Parameters
        ----------
        new_item: (OPNewItemMixin, OPAbstractItem)
            An object inheriting from OPnewItemMixin and OPAbstractItem representing the populated template
            of the new item to create
        password_recipe: OPPasswordRecipe
            Where appropriate, the password recipe to pass to '--password=' when creating the item
        vault: str
            Name of the vault to assign the item to
        Raises
        ------
        OPInvalidItemException
            - If new_item does not inherit from OPNewItemMixin
            - if password_recipe is provided and new_item does not support passwords
                (currently only Login and Password item types support passwords)
        OPItemCreateException
            If item creation fails for any reason during command execution

        Returns
        -------
        op_item: OPAbstractItem
            The newly created item object

        """
        if not isinstance(new_item, OPNewItemMixin):
            raise OPInvalidItemException(
                "Attempting to create item using object not from a template")

        # Most items don't support passwords. Only login & password items do
        # 'op' will fail if we provide a password recipe when creating an
        # an item that doesn't support passwords
        if password_recipe and not new_item.supports_passwords():
            raise OPInvalidItemException(
                "Password recpipe provided for an item that doesn't support passwords")
        result_str = super()._item_create(
            new_item, password_recipe=password_recipe, vault=vault)
        op_item = OPItemFactory.op_item(result_str)
        return op_item

    def login_item_create(self,
                          title: str,
                          username: str,
                          password: Union[str, OPPasswordRecipe] = None,
                          url: Optional[str] = None,
                          url_label: str = "Website",
                          vault=None):  # pragma: no coverage
        """
        Create a new login item in the authenticated 1Password account

        Parameters
        ----------
        Title : str
            User viewable name of the login item to create
        username : str
            username string for the new login item
        password : Union[str, OPPasswordRecipe], optional
            May be one of:
                - the literal password string to set for this login item
                - a OPPasswordRecipe object that will be provided to '--generate-password='
            If a password string is provided that password will be set for this login item
            If an OPPasswordRecipe object is provided, it will ensure a well-formed password recipe string is provided to '--generate-password='
        url: str, optional
            If provided, set to the primary URL of the login item

        Raises
        ------
        OPInvalidItemException
            - If new_item does not inherit from OPNewItemMixin
            - if password_recipe is provided and new_item does not support passwords
                (currently only Login and Password item types support passwords)
        OPItemCreateException
            If item creation fails for any reason during command execution

        Returns
        -------
        login_item: OPLoginItem
            The newly created login item object
        """
        password_recipe = None

        # if password is actually a password recipe,
        # set passsword_recipe and set password to None
        # that way we don't pass it into OPLoginItemTemplate
        # and instead pass it to _item_create() so it gets used on the command line
        if isinstance(password, OPPasswordRecipe):
            password_recipe = password
            password = None

        if url:
            url_obj = OPLoginItemNewPrimaryURL(url, url_label)
        new_item = OPLoginItemTemplate(
            title, username, password=password, url=url_obj)
        login_item = self.item_create(
            new_item, password_recipe=password_recipe, vault=vault)
        return login_item

    def item_delete(self, item_identifier: str, vault: Optional[str] = None, archive: bool = False) -> str:
        """
        Delete an item based on title or unique identifier

        Parameters
        ----------
        item_identifier: str
            Any item identifier accepted by 'op item delete'
            Generally this includes item name/title, item ID, or share link
            See 'op item get --help' for more information
        vault: str, optional
            The name or ID of a vault to override the default vault
        archive: bool
            Whether to archive or permanently delete the item

        Note:
            If a non-unique item identifier is provided (e.g., item name/title), and there
            is more than one item that matches, OPItemDeleteException will be raised. Check the
            error message in OPItemDeleteException.err_output for details

        Raises
        ------
        OPItemDeleteException
            - If the item to be deleted is not found
            - If there is more than one item matching 'item_identifier'
            - If the delete operation fails for any other reason

        Returns
        -------
        item_id: str
            Unique identifier of the item deleted

        """
        try:
            output = super()._item_get(item_identifier, vault=vault)
            item = _OPGenericItem(output)
        except OPItemGetException as e:
            raise OPItemDeleteException.from_opexception(e)
        # we want to return the explicit ID even if we were
        # given an item title or other identifier
        # that way the caller knows exactly what got deleted
        # can match it up with what they expected to be deleted, if desired
        item_id = item.unique_id

        # 'op item delete' doesn't have any stdout, so we're not
        # capturing any here
        self._item_delete(item_id, vault=vault, archive=archive)

        return item_id

    def signed_in_accounts(self, decode="utf-8") -> OPAccountList:
        account_list_json = super()._signed_in_accounts(self.op_path, decode=decode)
        account_list = OPAccountList(account_list_json)
        return account_list

    def signout(self, forget=False):  # pragma: no coverage
        """
        Sign out of the account used to create this OP instance
        This is equivalent to the command 'op signout'
        Parameters
        ----------
        forget: bool, optional
            Optionally remove details for this 1Password account from this device.
            This is equivalent to the command 'op signout --forget'

        Raises
        ------
        OPSignoutException
            If the signout operation fails for any reason
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        None
        """
        account = self._account_identifier
        token = self.token
        if not token and not self._uses_bio:
            return

        try:
            super()._signout(account, token, forget=forget)
        except OPCmdFailedException as ocfe:
            raise OPSignoutException.from_opexception(ocfe) from ocfe

        # drop any reference to op session token identifier from this
        # instance and from environment variables
        self._sanitize()

    @classmethod
    def forget(cls, account: str, op_path=None):  # pragma: no coverage
        """
        Remove details for the specified account from this device
        This is equivalent to the command 'op forget <account>'

        Note: this is a class method, so there is no need to have an OP instance or to have
        an active, signed-in session

        Parameters
        ----------
        account : str
            The account shorthand to forget
        op_path: str, optional
            Path to an 'op' executable to use for this action

        Raises
        ------
        OPForgetException
            If the lookup fails for any reason
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        None
        """

        try:
            cls._forget(account, op_path=op_path)
        except OPCmdFailedException as ocfe:
            raise OPForgetException.from_opexception(ocfe) from ocfe

    def _sanitize(self):  # pragma: no coverage
        self._token = None
        if self._sess_var:
            try:
                env.pop(self._sess_var)
            except KeyError:
                pass
