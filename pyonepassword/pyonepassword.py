from __future__ import annotations

import fnmatch
import logging
from os import environ as env
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Type, Union

if TYPE_CHECKING:  # pragma: no coverage
    from .op_items.fields_sections.item_field import OPItemField

from ._field_assignment import OPFieldTypeEnum
from ._op_commands import (
    EXISTING_AUTH_IGNORE,
    ExistingAuthEnum,
    _OPCommandInterface
)
from .account import OPAccountList
from .op_items._item_list import OPItemList
from .op_items._item_type_registry import OPItemFactory
from .op_items._new_item import OPNewItemMixin
from .op_items.fields_sections.item_field import OPConcealedField
from .op_items.fields_sections.item_section import OPFieldNotFoundException
from .op_items.item_types._item_base import (
    OPAbstractItem,
    OPSectionNotFoundException
)
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
    OPDocumentEditException,
    OPDocumentGetException,
    OPFieldExistsException,
    OPForgetException,
    OPInsecureOperationException,
    OPInvalidDocumentException,
    OPInvalidItemException,
    OPItemDeleteException,
    OPItemDeleteMultipleException,
    OPItemEditException,
    OPItemGetException,
    OPItemListException,
    OPPasswordFieldDowngradeException,
    OPSignoutException,
    OPUserEditException,
    OPUserGetException
)
from .string import RedactedString
from .version import PyOPAboutMixin


class OP(_OPCommandInterface, PyOPAboutMixin):
    """
    Class for logging into and querying a 1Password account via the 'op' cli command.
    """

    def __init__(self,
                 account: Optional[str] = None,
                 password: Optional[str] = None,
                 existing_auth: ExistingAuthEnum = EXISTING_AUTH_IGNORE,
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

    def document_edit(self,
                      document_identifier: str,
                      file_path_or_document_bytes: Union[str, Path, bytes],
                      file_name: Optional[str] = None,
                      new_title: Optional[str] = None,
                      vault: Optional[str] = None,
                      relaxed_validation: bool = False) -> str:
        """
        Edit a document object based on document name or unique identifier

        Parameters
        ----------
        document_identifier : str
            Name or identifier of the document to edit
        file_path_or_document_bytes: Union[str, Path, bytes],
            Either the path to the file to replace the current document with,
            or the actual bytes representation of the replacement document
        file_name: str, optional
            Optionally set the document's fileName attribute to this value
        new_title: str, optional
            Optionally update the title of the document to this value
        vault : str, optional
            The name or ID of a vault to override the default vault, by default None
        relaxed_validation: bool, optional
            Whether to enable relaxed item validation for this query, in order to parse non-conformant data
            by default False
        Returns
        -------
        document_id: str
            Unique identifier of the item edited

        Raises
        ------
        OPDocumentEditException
            - If the document to be edit is not found
            - If there is more than one item matching 'document_identifier'
            - If the edit operation fails for any other reason

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """

        if isinstance(file_path_or_document_bytes, bytes):
            document_bytes = file_path_or_document_bytes
        else:
            file_path_or_document_bytes = Path(file_path_or_document_bytes)
            document_bytes = file_path_or_document_bytes.read_bytes()

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
            raise OPDocumentEditException.from_opexception(e)
        # we want to return the explicit ID even if we were
        # given an document name or other identifier
        # that way the caller knows exactly what got edited
        # can match it up with what they expected to be edited, if desired
        document_id = item.unique_id

        # 'op document edit' doesn't have any stdout, so we're not
        # capturing any here
        self._document_edit(document_id, document_bytes,
                            file_name=file_name, new_title=new_title, vault=vault)

        return document_id

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

    def login_item_create(self,
                          title: str,
                          username: str,
                          password: Union[str, OPPasswordRecipe] = None,
                          url: Optional[str] = None,
                          url_label: str = "Website",
                          tags: Optional[List[str]] = None,
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
        if tags is None:
            tags = list()
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

    def item_edit_add_password_field(self,
                                     item_identifier: str,
                                     password: str,
                                     field_label: str,
                                     section_label: Optional[str] = None,
                                     vault: Optional[str] = None,
                                     insecure_operation: bool = False):
        """
        Add new concealed/passwrod field and optionally a new section to an item

        Parameters
        ----------
        item_identifier: str
            The item to edit
        value: str
            The password value to set
        field_label: str
            The human readable label of the field to create
        section_label: str, optional
            If provided, the human readable section label the field is associated with.
            It will be created if it doesn't exist
        vault: str, optional
            The name or ID of a vault containing the item to edit
            Overrides the OP object's default vault, if set
        insecure_operation: bool
            Caller acknowledgement of the insecure nature of this operation
            by default, False

        Raises
        ------
        OPFieldExistsException
            If the field to be added already existss
        OPItemEditException
            If the item edit operation fails for any reason
        Returns
        -------
        op_item: OPAbstractItem
            The edited version of the item

        NOTE: an 'item_get()` operation first is performed in order to validate
              the field name and, if provided, section name


        NOTE: The following scenarios are an error
            - An ambiguous existing field match:
                one or more fields match the field label and no section label was specified
            - An explicit existing field match:
                one or more field/section pairings exist that match the field label & section label
        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """

        password = RedactedString(password, unmask_len=0)
        field_type = OPFieldTypeEnum.PASSWORD
        op_item = self._item_edit_set_field(item_identifier,
                                            field_type,
                                            field_label,
                                            section_label,
                                            password,
                                            vault,
                                            password_downgrade=False,
                                            insecure_operation=insecure_operation,
                                            create_field=True)
        return op_item

    def item_edit_add_url_field(self,
                                item_identifier: str,
                                url: str,
                                field_label: str,
                                section_label: Optional[str] = None,
                                vault: Optional[str] = None):
        """
        Add new URL field and optionally a new section to an item

        NOTE: This method differs from item_edit_url(). This method adds a URL item field
        whereas item_edit_url() sets the URL property, which is not a field at all, on a login item

        Parameters
        ----------
        item_identifier: str
            The item to edit
        url: str
            The URL value to set
        field_label: str
            The human readable label of the field to create
        section_label: str, optional
            If provided, the human readable section label the field is associated with.
            It will be created if it doesn't exist
        vault: str, optional
            The name or ID of a vault containing the item to edit
            Overrides the OP object's default vault, if set

        Raises
        ------
        OPFieldExistsException
            If the field to be added already existss
        OPItemEditException
            If the item edit operation fails for any reason
        Returns
        -------
        op_item: OPAbstractItem
            The edited version of the item

        NOTE: an 'item_get()` operation first is performed in order to validate
              the field name and, if provided, section name


        NOTE: The following scenarios are an error
            - An ambiguous existing field match:
                one or more fields match the field label and no section label was specified
            - An explicit existing field match:
                one or more field/section pairings exist that match the field label & section label
        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """
        field_type = OPFieldTypeEnum.URL
        op_item = self._item_edit_set_field(item_identifier,
                                            field_type,
                                            field_label,
                                            section_label,
                                            url,
                                            vault,
                                            password_downgrade=False,
                                            insecure_operation=False,
                                            create_field=True)
        return op_item

    def item_edit_add_text_field(self,
                                 item_identifier: str,
                                 value: str,
                                 field_label: str,
                                 section_label: Optional[str] = None,
                                 vault: Optional[str] = None):
        """
        Add new text field and optionally a new section to an item

        Parameters
        ----------
        item_identifier: str
            The item to edit
        value: str
            The text value to set
        field_label: str
            The human readable label of the field to create
        section_label: str, optional
            If provided, the human readable section label the field is associated with.
            It will be created if it doesn't exist
        vault: str, optional
            The name or ID of a vault containing the item to edit
            Overrides the OP object's default vault, if set

        Raises
        ------
        OPFieldExistsException
            If the field to be added already existss
        OPItemEditException
            If the item edit operation fails for any reason
        Returns
        -------
        op_item: OPAbstractItem
            The edited version of the item

        NOTE: an 'item_get()` operation first is performed in order to validate
              the field name and, if provided, section name


        NOTE: The following scenarios are an error
            - An ambiguous existing field match:
                one or more fields match the field label and no section label was specified
            - An explicit existing field match:
                one or more field/section pairings exist that match the field label & section label
        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """
        field_type = OPFieldTypeEnum.TEXT
        op_item = self._item_edit_set_field(item_identifier,
                                            field_type,
                                            field_label,
                                            section_label,
                                            value,
                                            vault,
                                            password_downgrade=False,
                                            insecure_operation=False,
                                            create_field=True)
        return op_item

    def item_edit_set_password(self,
                               item_identifier: str,
                               password: str,
                               field_label: str = "password",
                               section_label: Optional[str] = None,
                               vault: Optional[str] = None,
                               insecure_operation: bool = False,):
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
        vault: str, optional
            The name or ID of a vault containing the item to edit
            Overrides the OP object's default vault, if set
        insecure_operation: bool
            Caller acknowledgement of the insecure nature of this operation
            by default, False

        Raises
        ------
        OPSectionNotFoundException
            If a section label is specified but can't be looked up on the item object
        OPFieldNotFoundException
            If the field label can't be looked up on the item object
        OPItemEditException
            If the item edit operation fails for any reason
        OPInsecureOperationException
            If the caller does not pass insecure_operation=True, failing to acknowledge the
            insecure nature of this operation
        Returns
        -------
        op_item: OPAbstractItem
            The edited version of the item

        Note: an 'item_get()` operation first is performed in order to validate
              the field name and, if provided, section name

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """

        # TODO: look up item and validate section and field
        password = RedactedString(password, unmask_len=0)
        field_type = OPFieldTypeEnum.PASSWORD
        op_item = self._item_edit_set_field(item_identifier,
                                            field_type,
                                            field_label,
                                            section_label,
                                            password,
                                            vault,
                                            password_downgrade=False,
                                            insecure_operation=insecure_operation,
                                            create_field=False)
        return op_item

    def item_edit_set_url_field(self,
                                item_identifier: str,
                                url: str,
                                field_label: str,
                                section_label: Optional[str] = None,
                                vault: Optional[str] = None,
                                password_downgrade: bool = False):
        """
        Set a new value on an existing item's URL field

        NOTE: This method differs from item_edit_url(). This method sets a URL value on an
        existing item field whereas item_edit_url() sets the URL property, which is not a
        field at all, on a login item

        Parameters
        ----------
        item_identifier: str
            The item to edit
        url: str
            The URL value to set
        field_label: str
            The human readable label of the field to edit
        section_label: str, optional
            If provided, the human readable section label the field is associated with
        vault: str, optional
            The name or ID of a vault containing the item to edit
            Overrides the OP object's default vault, if set
        password_downgrade: bool
            Whether and existing concealed (i.e., password) field should be downgraded to a non-password
            field.
            If the existing field IS concealed and this value is false, an exception will be raised

        Raises
        ------
        OPSectionNotFoundException
            If a section label is specified but can't be looked up on the item object
        OPFieldNotFoundException
            If the field label can't be looked up on the item object
        OPPasswordFieldDowngradeException
            If the field is a concealed field and password_downgrade is False
        OPItemEditException
            If the item edit operation fails for any reason
        Returns
        -------
        op_item: OPAbstractItem
            The edited version of the item

        Note: an 'item_get()` operation first is performed in order to validate
              the field name and, if provided, section name

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault

        NOTE: Neither 1Password nor pyonepassword perform any validation on the URL
              string. It may be virtually any string.

        """

        # If section or field not found, will raise
        # OPSectionNotFoundException, or
        # OPFieldNotFoundException

        field_type = OPFieldTypeEnum.URL
        op_item = self._item_edit_set_field(item_identifier,
                                            field_type,
                                            field_label,
                                            section_label,
                                            url,
                                            vault,
                                            password_downgrade,
                                            insecure_operation=False,
                                            create_field=False)
        return op_item

    def item_edit_set_text_field(self,
                                 item_identifier: str,
                                 value: str,
                                 field_label: str,
                                 section_label: Optional[str] = None,
                                 vault: Optional[str] = None,
                                 password_downgrade: bool = False):
        """
        Set a new value on an existing item's text field

        Parameters
        ----------
        item_identifier: str
            The item to edit
        value: str
            The text value to set
        field_label: str
            The human readable label of the field to edit
        section_label: str, optional
            If provided, the human readable section label the field is associated with
        vault: str, optional
            The name or ID of a vault containing the item to edit
            Overrides the OP object's default vault, if set
        password_downgrade: bool
            Whether and existing concealed (i.e., password) field should be downgraded to a non-password
            field.
            If the existing field IS concealed and this value is false, an exception will be raised

        Raises
        ------
        OPSectionNotFoundException
            If a section label is specified but can't be looked up on the item object
        OPFieldNotFoundException
            If the field label can't be looked up on the item object
        OPPasswordFieldDowngradeException
            If the field is a concealed field and password_downgrade is False
        OPItemEditException
            If the item edit operation fails for any reason
        Returns
        -------
        op_item: OPAbstractItem
            The edited version of the item

        Note: an 'item_get()` operation first is performed in order to validate
              the field name and, if provided, section name

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """

        # If section or field not found, will raise
        # OPSectionNotFoundException, or
        # OPFieldNotFoundException

        field_type = OPFieldTypeEnum.TEXT
        op_item = self._item_edit_set_field(item_identifier,
                                            field_type,
                                            field_label,
                                            section_label,
                                            value,
                                            vault,
                                            password_downgrade,
                                            insecure_operation=True,
                                            create_field=False)
        return op_item

    def item_edit_delete_field(self,
                               item_identifier: str,
                               field_label: str,
                               section_label: Optional[str] = None,
                               vault: Optional[str] = None):
        """
        Delete a field, and optionally a section from an item

        If a section is specified, and it has no remaining fields after
        the edit operation, the section will be removed as well

        Parameters
        ----------
        item_identifier: str
            The item to edit
        field_label: str
            The human readable label of the field to delete
        section_label: str, optional
            If provided, the human readable section label the field is associated with
        vault: str, optional
            The name or ID of a vault containing the item to edit
            Overrides the OP object's default vault, if set

        Raises
        ------
        OPItemGetException
            If the item lookup fails for any reason
        OPSectionNotFoundException
            If a section label is specified but can't be looked up on the item object
        OPFieldNotFoundException
            If the field label can't be looked up on the item object
        OPItemEditException
            If the item edit operation fails for any reason
        Returns
        -------
        op_item: OPAbstractItem
            The edited version of the item

        Note: an 'item_get()` operation first is performed in order to validate
              the field name and, if provided, section name

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault

        """

        # If section or field not found, will raise
        # OPSectionNotFoundException, or
        # OPFieldNotFoundException

        VALUE_NONE = None
        PASSWORD_DOWNGRADE_IGNORE = True
        INSECURE_OPERATION = False
        field_type = OPFieldTypeEnum.DELETE
        op_item = self._item_edit_set_field(item_identifier,
                                            field_type,
                                            field_label,
                                            section_label,
                                            VALUE_NONE,
                                            vault,
                                            PASSWORD_DOWNGRADE_IGNORE,
                                            INSECURE_OPERATION,
                                            create_field=False)
        return op_item

    def item_edit_favorite(self,
                           item_identifier: str,
                           favorite: bool,
                           vault: Optional[str] = None):
        """
        Set or unset an item's 'favorite' status

        Parameters
        ----------
        item_identifier: str
            The item to edit
        favorite: bool
            Whether to set or unset the item's favorite status
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
        Supported
        """
        result_str = self._item_edit_favorite(item_identifier,
                                              favorite,
                                              vault=vault)
        op_item = OPItemFactory.op_item(result_str, generic_okay=True)

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
        Supported
        """

        result_str = self._item_edit_generate_password(item_identifier,
                                                       password_recipe,
                                                       vault)
        op_item = OPItemFactory.op_item(result_str, generic_okay=True)
        return op_item

    def item_edit_tags(self,
                       item_identifier: str,
                       tags: List[str],
                       append_tags: bool = False,
                       vault: Optional[str] = None) -> OPAbstractItem:
        """
        Replace, append, or remove an item's tags

        Parameters
        ----------
        item_identifier: str
            The item to edit
        tags: List[str]
            The list of tags to assign to the item
        append_tags: bool
            Append to the existing list of tags or replace the existing list
            by default True
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

        Note: an 'item_get()` operation first is performed in order to obtain the
              existing set of tags

        Service Account Support
        -----------------------
        Supported
          required keyword arguments: vault
        """
        item = self.item_get(item_identifier, vault=vault)
        if append_tags:
            existing_tags = item.tags
            for tag in tags:
                if tag not in existing_tags:
                    # although op item tags *sort of* behave as a set
                    # they are technically a list and preserve order
                    # so lets go to the trouble to also preserve order
                    # and not append any duplicates
                    existing_tags.append(tag)
                tags = existing_tags
        else:
            item = None

        result_str = self._item_edit_tags(item_identifier,
                                          tags,
                                          vault=vault)
        op_item = OPItemFactory.op_item(result_str, generic_okay=True)

        return op_item

    def item_edit_title(self,
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
        Supported
            required keyword arguments: vault
        """
        self.item_get(item_identifier,
                      vault=vault)
        result_str = self._item_edit_title(item_identifier,
                                           item_title,
                                           vault=vault)
        op_item = OPItemFactory.op_item(result_str, generic_okay=True)

        return op_item

    def item_edit_url(self,
                      item_identifier: str,
                      url: str,
                      vault: Optional[str] = None):
        """
        Set the URL associated with an existing item

        NOTE: This method differs from item_edit_set_url_field(). This method sets the URL
        property on a login item and does not set values on any item fields

        Parameters
        ----------
        item_identifier: str
            The item to edit
        url: str
            The new URL to assign to the item
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
        Supported
        """
        result_str = self._item_edit_url(item_identifier,
                                         url,
                                         vault=vault)
        op_item = OPItemFactory.op_item(result_str, generic_okay=True)

        return op_item

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
                             categories: Optional[List[str]] = None,
                             include_archive: bool = False,
                             tags: Optional[List[str]] = None,
                             archive: bool = False,
                             title_glob: str = None,
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
        title_glob: str, optional
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
        if tags is None:
            tags = list()
        if categories is None:
            categories = list()

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
                # we have to raise OPItemDeleteMultipleException from here
                # so we can give it the list of successully deleted items
                # that isn't known from inside _item_delete_multiple()
                raise OPItemDeleteMultipleException.from_opexception(
                    ope, deleted_items)
            deleted_items.extend(batch)

        return deleted_items

    def item_list(self,
                  categories: Optional[List[str]] = None,
                  include_archive: bool = False,
                  tags: Optional[List[str]] = None,
                  title_glob: str = None,
                  vault: str = None,
                  generic_okay: bool = True) -> OPItemList:
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
        title_glob: str, optional
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
        if tags is None:
            tags = list()
        if categories is None:
            categories = list()

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

    def user_edit(self,
                  user_name_or_id: str,
                  new_name: Optional[str] = None,
                  travel_mode: Optional[bool] = None) -> str:
        """
        Edit the details for the user specified by name or unique ID.

        Parameters
        ----------
        user_name_or_id: str
            Name or ID of the user to edit
        new_name: str, optional
            New user-visible name to assign to user
            by default, None
        travel_mode: bool, optional
            Set travel mode on or off
            by default, None
        Raises
        ------
        OPUserEditException
            If the lookup or edit fails for any reason during command execution
        OPNotFoundException
            If the 1Password command can't be found

        Returns
        -------
        user_id: str
            The unique ID of the user

        Service Account Support
        -----------------------
        Not supported
        """
        # 'op document edit' doesn't have any stdout, so we're not
        # capturing any here
        try:
            user = self.user_get(user_name_or_id)
        except OPUserGetException as e:
            raise OPUserEditException.from_opexception(e)

        user_id = user.unique_id
        self._user_edit(user_id, new_name, travel_mode)

        return user_id

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

    def _item_edit_set_field(self,
                             item_identifier: str,
                             field_type: OPFieldTypeEnum,
                             field_label: str,
                             section_label: str,
                             value: str,
                             vault: Optional[str],
                             password_downgrade: bool,
                             insecure_operation: bool,
                             create_field: bool):
        """
        Set a new value on an existing item field

        This is intended to be a centralized Section.Field[field_type]=value call site

        It allows us to do validation in a central location, including:
        - verifying the item we're trying to edit actually exists
        - verifying the field and section we're trying to edit actually exist
        - verify we don't accidentally downgrade a password field to some non-protected field

        This also allows us to ensure we relax the following restrictions for item editing:
        - generic_okay = True

        The point is that we don't need to remember to do the verification steps
        every time we add an item-edit public method
        """

        # if we're assigning a password, caller needs to pass insecure_operation=True
        if field_type == OPFieldTypeEnum.PASSWORD and not insecure_operation:
            msg = "Password assignment via 'op item edit' is inherently insecure. Pass 'insecure_operation=True' to override. For more information, see https://developer.1password.com/docs/cli/reference/management-commands/item#item-edit"
            self.logger.fatal(msg)
            raise OPInsecureOperationException(msg)

        # Does the item exist?
        # generic_okay: Enable editing of unknown OPItem types
        try:
            item = self.item_get(
                item_identifier, vault=vault, generic_okay=True)
        except OPItemGetException as e:
            raise OPItemEditException.from_opexception(e)

        if not create_field:
            # Does the field and, if provided, the section exist?
            # Don't accidentally create a new field or section
            # if the field or, if provided, section are not found
            # OPFieldNotFoundException or OPSectionNotFoundException will
            # be raised here
            field = self._validate_item_field_exists(
                item, field_label, section_label)

            # If the existing field is a password, don't accidentally
            # turn it into an unprotected text (or other type) of field
            if isinstance(field, OPConcealedField):
                if field_type != OPFieldTypeEnum.PASSWORD and not password_downgrade:
                    msg = "Item edit operation would downgrade field from a password field to a non-password field."
                    raise OPPasswordFieldDowngradeException(msg)
        else:
            # We're explicitly creating a new field so let's make sure
            # one with this label and section doesn't already exist
            # otherwise we'll accidently edit that one instead
            # this will raise
            self._validate_item_field_does_not_exist(
                item, field_label, section_label)

        item_json = self._item_edit_set_field_value(item_identifier,
                                                    field_type,
                                                    value,
                                                    field_label,
                                                    section_label=section_label,
                                                    vault=vault)

        # generic_okay: Enable editing of unknown OPItem types
        # relaxed_validation: Enable editing of non-conforming items
        item = OPItemFactory.op_item(
            item_json, generic_okay=True)
        return item

    def _validate_item_field_exists(self,
                                    item: OPAbstractItem,
                                    field_label: str,
                                    section_label: Optional[str]) -> OPItemField:
        # Validate that the field and, if provided, section exist
        # It is an error if any:
        #   - If provided, a section with the given label is not found
        #   - A field with the given label is not found
        #   - If no section label is specified, no matching field lacks an attached section
        #
        # Success if any:
        #   - If a section label is specified and all of:
        #       - At least one matching section is found
        #       - At least one matching field is found field is found
        #       - At least one (section, field) paring is found among the matching sections and fields
        #   - If no section label is specified
        #       - A matching field is found that has no associated section

        field = None
        section_ids = set()
        if section_label:
            # this may raise OPSectionNotFoundException if there is no match
            # this is expected. It is up to the caller to handle this
            sections = item.sections_by_label(section_label)
            for _section in sections:
                section_ids.add(_section.section_id)

        # this may raise OPFieldNotfoundException if there is no match
        # this is expected. It is up to the caller to handle this
        fields = item.fields_by_label(field_label)

        for _field in fields:
            if _field.section_id and section_label:
                if _field.section_id in section_ids:
                    # We found a matching field
                    # it has a section that matches one of the known matching sections
                    # This is good: at least one (section, field) pairing exists
                    field = _field
                    break
            elif not _field.section_id and not section_label:
                # we found a matching field
                # it doesn't have a section and we were told not to look for a section
                # This is good: a (<no section>, field) pairing exists
                field = _field
                break

        if not field:
            if not section_label:
                msg = f"No field found '{field_label}' that lacks a section"
                raise OPFieldNotFoundException(msg)
            else:
                msg = f"Section '{section_label}', field '{field_label}' not found"
                raise OPFieldNotFoundException(msg)
        return field

    def _validate_item_field_does_not_exist(self,
                                            item: OPAbstractItem,
                                            field_label: str,
                                            section_label: Optional[str]) -> None:
        # Raises OPFieldExistsException if:
        # - Ambiguous match: one or more fields match the field label and no section label was specified
        # - Explicit match: one or more field/section pairings exist that match the field label & section label
        #
        # Success if any of:
        # - No fields matching the field label are found
        # - A section label is specified but a matching section is not found
        # - A section label is specified and section found,
        #       but no matching fields found are associated with it
        verified = False
        if not section_label:
            # ensure section label is not an empty string or some other "false" value
            section_label = None
        while not verified:
            section_ids = set()
            try:
                fields = item.fields_by_label(field_label)
            except OPFieldNotFoundException:
                # no fields found with the specified label
                # this is good: the field does not exist
                verified = True
                break

            if section_label:
                try:
                    sections = item.sections_by_label(section_label)
                    for section in sections:
                        section_ids.add(section.section_id)
                except OPSectionNotFoundException:
                    # we were explicitly given a section to look up and we didn't find it
                    # so this is good: the (section, field) paring does not exist
                    verified = True
                    break

            if fields and not section_label:
                # a field exists, and without being explicit about the section
                # 'op' may still match the field whether or not it has a section
                # this is bad: a field exists and may be ambigously matched
                raise OPFieldExistsException(
                    f"Field \"{field_label}\" exists and no section was specified")

            for field in fields:
                if field.section_id in section_ids:
                    msg = f"Section: \"{section_label}\", "
                    msg += f"field: \"{field_label}\" already exists"
                    # we were explicitly given a section to look up and we found it AND the field
                    # this is bad: at least one (section, field) DOES exist
                    raise OPFieldExistsException(msg)

            # None of the fields found match any of the sections found
            # This is good: a (section, field) paring could not be found
            verified = True
            break
