import fnmatch
import logging
from os import environ as env
from typing import List, Optional, Type, Union

from ._py_op_commands import (
    EXISTING_AUTH_IGNORE,
    ExistingAuthEnum,
    _OPCommandInterface
)
from ._py_op_deprecation import deprecated_kwargs
from .account import OPAccountList
from .op_items._item_list import OPItemList
from .op_items._item_type_registry import OPItemFactory
from .op_items._new_item import OPNewItemMixin
from .op_items.item_types._item_base import OPAbstractItem
from .op_items.item_types.generic_item import (
    _OPGenericItem,
    _OPGenericItemRelaxedValidation
)
from .op_items.item_types.login import (
    OPLoginItemNewPrimaryURL,
    OPLoginItemTemplate
)
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
    OPInsecureOperationException,
    OPInvalidDocumentException,
    OPInvalidItemException,
    OPItemDeleteException,
    OPItemDeleteMultipleException,
    OPItemGetException,
    OPItemListException,
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
        OPAuthenticationException
            if:
                - No previous authentication (e.g., existing session or service account otken) is available
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

    def item_get(self, item_identifier, vault=None, include_archive=False, generic_okay=False, relaxed_validation=False) -> OPAbstractItem:
        """
        Get an 'item' object from a 1Password vault.
        The returned object may be any of the item types extending OPAbstractItem.
        These currently include:
        - OPLoginItem
        - OPCreditCardItem
        - OPSecureNoteItem
        - OPPasswordItem
        - OPDocumentItem
        - OPServerItem
        - OPDatabaseItem

        Note that getting a document item is not the same as getting the document itself. The
        item only contains metadata about the document such as filename.

        Parameters
        ----------
        item_identifier: str
            Name or ID of the item to look up
        vault: str, optional
            The name or ID of a vault to override the object's default vault, by default None
        include_archive: bool, optional
            Include items in the Archive, by default False
        generic_okay: bool, optional
            Instantiate unknown item types as _OPGenericItem rather than raise OPUnknownItemException
        relaxed_validation: bool, optional
            Whether to enable relaxed item validation for this query, in order to parse non-conformant data
            by default False
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
            If the item object returned by 1Password isn't a known type and generic_okay is False
        OPNotFoundException
            If the 1Password command can't be found
        Returns
        -------
        item: OPAbstractItem
            An item object of one of the types listed above

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """

        output = self._item_get(item_identifier, vault=vault,
                                decode="utf-8", include_archive=include_archive)
        op_item = OPItemFactory.op_item(
            output, generic_okay=generic_okay, relaxed_validation=relaxed_validation)
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

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """
        output = self._item_get_totp(
            item_identifier, vault=vault, decode="utf-8")
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

        Service Account Support
        -----------------------
        Supported
        """
        user_json = self._user_get(user_name_or_id)
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

        Service Account Support
        -----------------------
        Supported
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

        Service Account Support
        -----------------------
        Supported
            prohibited keyword arguments: group, user
        """
        vault_json = self._vault_get(vault_name_or_id, decode="utf-8")
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

        Service Account Support
        -----------------------
        Supported
        """
        vault_list_json = self._vault_list(
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

        Service Account Support
        -----------------------
        Supported
        """
        group_json = self._group_get(group_name_or_id, decode="utf-8")
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

        Service Account Support
        -----------------------
        Supported
        """
        group_list: Union[str, OPGroupDescriptorList]
        group_list = self._group_list(
            user_name_or_id=user_name_or_id, vault=vault)
        group_list = OPGroupDescriptorList(group_list)
        return group_list

    def item_get_password(self, item_identifier, vault=None, relaxed_validation=False) -> str:
        """
        Get the value of the password field from the item specified by name or UUID.

        Parameters
        ----------
        item_identifier: str
            The item to look up
        vault: str, optional
            The name or ID of a vault to override the object's default vault
        relaxed_validation: bool, optional
            Whether to enable relaxed item validation for this query, in order to parse non-conformant data
            by default False

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

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """
        item: OPAbstractItem
        item = self.item_get(item_identifier, vault=vault,
                             relaxed_validation=relaxed_validation)

        # satisfy 'mypy': OPAbstractItem has no "password" attribute
        if not hasattr(item, "password"):
            raise OPInvalidItemException(
                f"Item: {item.title} has no password attribute")
        else:
            password = item.password
        return password

    def item_get_filename(self, item_identifier, vault=None, include_archive=False, relaxed_validation=False):
        """
        Get the fileName attribute a document item from a 1Password vault by name or UUID.

        Parameters
        ----------
        item_identifier: str
            The item to look up
        vault: str, optional
            The name or ID of a vault to override the object's default vault
        relaxed_validation: bool, optional
            Whether to enable relaxed item validation for this query, in order to parse non-conformant data
            by default False
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

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """
        item = self.item_get(item_identifier, vault=vault,
                             include_archive=include_archive, relaxed_validation=relaxed_validation)

        # raise AttributeError if item isn't a OPDocumentItem
        # we have to raise it ourselves becuase mypy complains OPAbstractItem doesn't have
        # '.file_name'
        if hasattr(item, "file_name"):
            file_name = item.file_name
        else:
            raise AttributeError(
                f"{item.__class__.__name__} object has no attribute 'file_name'")

        return file_name

    def document_get(self, document_name_or_id, vault=None, include_archive=False, relaxed_validation=False):
        """
        Download a document object from a 1Password vault by name or UUID.

        Parameters
        ----------
        document_name_or_id : str
            The item to look up
        vault: str, optional
            The name or ID of a vault to override the object's default vault
        relaxed_validation: bool, optional
            Whether to enable relaxed item validation for this query, in order to parse non-conformant data
            by default False
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

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """
        try:
            file_name = self.item_get_filename(
                document_name_or_id, vault=vault, include_archive=include_archive, relaxed_validation=relaxed_validation)
        except AttributeError as ae:
            raise OPInvalidDocumentException(
                "Item has no 'fileName' attribute") from ae
        except OPCmdFailedException as ocfe:
            raise OPDocumentGetException.from_opexception(ocfe) from ocfe

        try:
            document_bytes = self._document_get(document_name_or_id,
                                                vault=vault, include_archive=include_archive)
        except OPCmdFailedException as ocfe:
            raise OPDocumentGetException.from_opexception(ocfe) from ocfe

        return (file_name, document_bytes)

    def document_delete(self, document_identifier: str, vault: Optional[str] = None, archive: bool = False, relaxed_validation: bool = False) -> str:
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
        relaxed_validation: bool, optional
            Whether to enable relaxed item validation for this query, in order to parse non-conformant data
            by default False
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

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """

        # to satisfy mypy
        generic_item_class: Type[_OPGenericItem]
        if relaxed_validation:
            generic_item_class = _OPGenericItemRelaxedValidation
        else:
            generic_item_class = _OPGenericItem

        try:
            output = self._item_get(document_identifier, vault=vault)
            item = generic_item_class(output)
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

    def item_list(self, categories=[], include_archive=False, tags=[], title_glob=None, vault=None, generic_okay=True) -> OPItemList:
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
        title_glob: bool, optional
            a shell-style glob pattern to match against item titles. If provided,
            resulting list will include only matching items
            by default None
        vault: str, optional
            The name or ID of a vault to override the object's default vault
        generic_okay: bool, optional
            Instantiate unknown item types as _OPGenericItem rather than raise OPUnknownItemException

        Raises
        ------
        OPItemListException
            If the user list operation for any reason during command execution
        OPUnknownItemTypeException
            If thelist returned by 1Password contains one or more item descriptors
            that aren't a known type and generic_okay is False
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        user: OPUserDescriptorList
            An object representing a list of user descriptors

        Service Account Support
        -----------------------
        Supported
        """
        item_list_json = self._item_list(
            categories, include_archive, tags, vault)
        item_list = OPItemList(item_list_json, generic_okay=generic_okay)

        if title_glob:
            _list = []
            for obj in item_list:
                if fnmatch.fnmatch(obj.title, title_glob):
                    _list.append(obj)
            item_list = OPItemList(_list)
        return item_list

    # TODO: Item creation is hard to test in an automated way since it results in changed
    #   state. There are operations during item creation that expect state to change from
    #   before to after item creation
    #   There is ongoing work in mock-op and mock-cli-framework to simulate changed state
    #   when this is complete these functions need to be tested
    #
    #   For now, ignore testing coverage
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

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
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
        result_str = self._item_create(
            new_item, password_recipe=password_recipe, vault=vault)
        op_item = OPItemFactory.op_item(result_str)
        return op_item

    def item_edit_generate_password(self,
                                    item_identifier: str,
                                    password_recipe: OPPasswordRecipe,
                                    vault: Optional[str] = None):
        """
        Generate and assign a new password for an existing item

        Parameters
        ----------
        item_identifier: str
            The item to edit
        password_recipe: OPPasswordRecipe
            The password recipe to apply when generating a new passwod
        vault: str, optional
            The name or ID of a vault containing the item to edit.
            Overrides the OP object's default vault, if set

        Raises
        ------
        OPItemEditException
            If the item edit operation fails for any reason

        Returns
        -------
        op_item: OPAbstractItem
            The edited version of the item

        Service Account Support
        -----------------------
        TODO placeholder text to satisfy pytest docstring checks
        """

        result_str = self._item_edit_generate_password(item_identifier,
                                                       password_recipe,
                                                       vault)
        op_item = OPItemFactory.op_item(result_str)
        return op_item

    def item_edit_set_password(self,
                               item_identifier: str,
                               password: str,
                               field_label: str = "password",
                               section_label: Optional[str] = None,
                               insecure_operation: bool = False,
                               vault: Optional[str] = None):
        """
        Assign a new password for an existing item

        SECURITY NOTE: This operation will include the provided password in cleartext as a command line argument
        to the 'op' command. On most platforms, the arguments, including the password, will be visible to other
        processes, including processes owned by other users
        In order to use this operaton, this insecurity must be acknowledged by passing the insecure_operation=True kwarg

        Parameters
        ----------
        item_identifier: str
            The item to edit
        password: str
            The password value to set
        field_label: str
            The human readable label of the field to edit
            by default "password"
        section_label: str, optional
            If provided, the human readable section label the field is associated with
        insecure_operation: bool
            Caller acknowledgement of the insecure nature of this operation
            by default, False
        vault: str, optional
            The name or ID of a vault containing the item to edit
            Overrides the OP object's default vault, if set

        Raises
        ------
        OPItemEditException
            If the item edit operation fails for any reason
        OPInsecureOperationException
            If the caller does not pass insecure_operation=True, failing to ackonowledge the
            insecure nature of this operation
        Returns
        -------
        op_item: OPAbstractItem
            The edited version of the item

        Service Account Support
        -----------------------
        TODO placeholder text to satisfy pytest docstring checks
        """
        if not insecure_operation:
            msg = "Password assignment via 'op item edit' is inherently insecure. Pass 'insecure_operation=True' to override. For more information, see https://developer.1password.com/docs/cli/reference/management-commands/item#item-edit"
            self.logger.fatal(msg)
            raise OPInsecureOperationException(msg)

        result_str = self._item_edit_set_password(item_identifier,
                                                  password,
                                                  field_label,
                                                  section_label=section_label,
                                                  vault=vault)
        op_item = OPItemFactory.op_item(result_str)
        return op_item

    def item_edit_set_title(self,
                            item_identifier: str,
                            item_title: str,
                            vault: Optional[str] = None):
        """
        Assign a new title for an existing item

        Parameters
        ----------
        item_identifier: str
            The item to edit
        item_title: str
            The new title to assign to the item
        vault: str, optional
            The name or ID of a vault containing the item to edit.
            Overrides the OP object's default vault, if set

        Raises
        ------
        OPItemEditException
            If the item edit operation fails for any reason

        Returns
        -------
        op_item: OPAbstractItem
            The edited version of the item

        Service Account Support
        -----------------------
        TODO placeholder text to satisfy pytest docstring checks
        """
        result_str = self._item_edit_set_title(item_identifier,
                                               item_title,
                                               vault=vault)
        op_item = OPItemFactory.op_item(result_str)

        return op_item

    def login_item_create(self,
                          title: str,
                          username: str,
                          password: Union[str, OPPasswordRecipe] = None,
                          url: Optional[str] = None,
                          url_label: str = "Website",
                          tags: List[str] = [],
                          vault: str = None):  # pragma: no coverage
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
        url_label: str, optional
            If provided and a URL is provided, this bcomes the primary URL's label
        tags: List[str], optional
            A list of tags to apply to the item when creating
        vault: str, optional
            The vault in which to create the new item

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

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """
        password_recipe = None

        # if password is actually a password recipe,
        # set passsword_recipe and set password to None
        # that way we don't pass it into OPLoginItemTemplate
        # and instead pass it to _item_create() so it gets used on the command line
        if isinstance(password, OPPasswordRecipe):
            password_recipe = password
            password = None

        url_obj = None
        if url:
            url_obj = OPLoginItemNewPrimaryURL(url, url_label)

        new_item = OPLoginItemTemplate(
            title, username, password=password, url=url_obj, tags=tags)

        login_item = self.item_create(
            new_item, password_recipe=password_recipe, vault=vault)
        return login_item

    def item_delete(self, item_identifier: str, vault: Optional[str] = None, archive: bool = False, relaxed_validation=False) -> str:
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

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """

        # to satisfy mypy
        generic_item_class: Type[_OPGenericItem]
        if relaxed_validation:
            generic_item_class = _OPGenericItemRelaxedValidation
        else:
            generic_item_class = _OPGenericItem

        try:
            output = self._item_get(item_identifier, vault=vault)
            item = generic_item_class(output)
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

    def item_delete_multiple(self,
                             vault,
                             categories=[],
                             include_archive=False,
                             tags=[],
                             archive=False,
                             title_glob=None,
                             batch_size=25):
        """
        Delete multiple items at once from a specific vault. This may take place across
        one or more 'op item delete' passes. A maximum "batch size" number of items to
        delete in each pass may optionally be specified (defaulting to 25)

        Parameters
        ----------
        vault: str
            The name or ID of a vault to delete from. This parameter is mandatory to mitigate
            the risk of deleting many items from the wrong vault
        include_archive: bool, optional
            Whether to include archived items for deleting
            by default False
        archive: bool
            Whether to archive or permanently delete the items
            by default False
        tags: List[str], optional
            A list of tags to restrict batch deletion to
        title_glob: bool, optional
            a shell-style glob pattern to match against item titles for deleting
            by default None
        batch_size: int, optional
            Maximum number of items to delete in each pass
            by default 25
            NOTE: The default batch size is subject to change without notice

        Note:
            If a non-unique item identifier is provided (e.g., item name/title), and there
            is more than one item that matches, OPItemDeleteException will be raised. Check the
            error message in OPItemDeleteException.err_output for details

        Raises
        ------
        OPItemDeleteMultipleException
            - If the 'item list' operation fails
            - If any of the 'item delete' operations fail

        Returns
        -------
        item_id: str
            Unique identifier of the item deleted

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """
        # track deleted items as we delete them so we can return
        # that list to the caller
        deleted_items = OPItemList([])

        try:
            item_list = self.item_list(categories=categories,
                                       include_archive=include_archive,
                                       tags=tags,
                                       title_glob=title_glob,
                                       vault=vault)
        except OPItemListException as e:
            raise OPItemDeleteMultipleException.from_opexception(
                e, deleted_items)

        batches: List[OPItemList] = []
        start = 0
        end = len(item_list)

        for i in range(start, end, batch_size):
            # split item list into chunks >= batch_size each
            x = i
            chunk = item_list[x:x+batch_size]
            batches.append(OPItemList(chunk))

        for batch in batches:
            batch_json = batch.serialize()
            try:
                self._item_delete_multiple(batch_json, vault, archive=archive)
            except OPCmdFailedException as ope:  # pragma: no coverage
                raise OPItemDeleteMultipleException.from_opexception(
                    ope, deleted_items)
            deleted_items.extend(batch)

        return deleted_items

    def signed_in_accounts(self, decode="utf-8") -> OPAccountList:
        """
        Retrieve a users and accounts set up on this device

        Returns
        -------
        OPAccountList
            List of accounts (subclass of List)

        Service Account Support
        -----------------------
        Supported
        """
        account_list_json = self._signed_in_accounts(
            self.op_path, decode=decode)
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

        Service Account Support
        -----------------------
        Supported
            Note: Has no effect on the authentication status of the service account currently in use
        """
        account = self._account_identifier
        token = self.token
        if not token and not self._uses_bio:
            return

        try:
            self._signout(account, token, forget=forget)
        except OPCmdFailedException as ocfe:
            raise OPSignoutException.from_opexception(ocfe) from ocfe

        # drop any reference to op session token identifier from this
        # instance and from environment variables
        self._sanitize()

    @classmethod
    def account_forget(cls, account: str, op_path=None):  # pragma: no coverage
        """
        Remove a 1Password account from this device
        This is equivalent to the command 'op account forget <account_id>'

        Note: this is a class method, so there is no need to have an OP instance or to have
        an active, signed-in session

        Note 2: this only removes accounts that have been added using 'op account add'.
        It has no effect on accounts accessed through 1Password app integration

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

        Service Account Support
        -----------------------
        Not supported
        """

        try:
            cls._account_forget(account, op_path=op_path)
        except OPCmdFailedException as ocfe:
            raise OPForgetException.from_opexception(ocfe) from ocfe

    def _sanitize(self):  # pragma: no coverage
        self._token = None
        if self._sess_var:
            try:
                env.pop(self._sess_var)
            except KeyError:
                pass
