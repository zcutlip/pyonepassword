# PYONEPASSWORD ITEM EDITING

As of version 4.0.0, `pyonepassword` support in-place item editing. There is API to match all of the operations supported by the `op item edit` command. This file describes the API as well as its restrictions and limitations.

The supported operations break down into two groups: operations that work with arbitrary item fields (and optionally sections), and ones that do not.

All of the methods described below are instance method on the `pyonepassword.OP` class.

## Non-field Editing Operations

> **Note**: Technically `OP.item_edit_generate_password()` operates on a field, but it only works on the built-in "password" field of Login and Password items.

`OP.item_edit_set_favorite()`

Set or unset an item's 'favorite' status

**Parameters**

`item_identifier`: `str`
    The item to edit
`favorite`: `bool`
    Whether to set or unset the item's favorite status
`vault`: `str`, optional
    The name or ID of a vault containing the item to edit.
    Overrides the OP object's default vault, if set

**Exceptions Raised**

`OPItemEditException`
    If the item edit operation fails for any reason

**Returns**

`op_item`: `OPAbstractItem`
    The edited version of the item

**Service account support**: supported

***

`OP.item_edit_generate_password()`

Generate and assign a new password for an existing item

**Parameters**

`item_identifier`: `str`
    The item to edit
`password_recipe`: `OPPasswordRecipe`
    The password recipe to apply when generating a new passwod
`vault`: `str`, optional
    The name or ID of a vault containing the item to edit.
    Overrides the OP object's default vault, if set

**Exceptions Raised**

`OPItemEditException`
    If the item edit operation fails for any reason

**Returns**

`op_item`: `OPAbstractItem`
    The edited version of the item

**Service account support**: supported

***

`OP.item_edit_set_title()`

Assign a new title for an existing item

**Parameters**

`item_identifier`: `str`
    The item to edit
`item_title`: `str`
    The new title to assign to the item
`vault`: `str`, optional
    The name or ID of a vault containing the item to edit.
    Overrides the OP object's default vault, if set

**Exceptions Raised**

`OPItemEditException`
    If the item edit operation fails for any reason

**Returns**

`op_item`: `OPAbstractItem`
    The edited version of the item

**Service account support**: supported, required keyword arguments: `vault`

***

`OP.item_edit_set_tags()`

Set or unset an item's tags

**Parameters**

`item_identifier`: `str`
    The item to edit
`tags`: `List`[str]
    The list of tags to assign to the item
`append_tags`: `bool`
    Append to the existing list of tags or replace the existing list
    by default True
`vault`: `str`, optional
    The name or ID of a vault containing the item to edit.
    Overrides the OP object's default vault, if set

**Exceptions Raised**

`OPItemEditException`
    If the item edit operation fails for any reason

**Returns**

`op_item`: `OPAbstractItem`
    The edited version of the item


**Service account support**: supported, required keyword arguments: vault

***

`OP.item_edit_set_url()`

Set the URL associated with an existing item

**NOTE**: This method differs from `item_edit_set_url_field()`. This method sets the URL
property on a login item and does not set values on any item fields

**Parameters**

`item_identifier`: `str`
    The item to edit
`url`: `str`
    The new URL to assign to the item
`vault`: `str`, optional
    The name or ID of a vault containing the item to edit.
    Overrides the OP object's default vault, if set

**Exceptions Raised**

`OPItemEditException`
    If the item edit operation fails for any reason

**Returns**

`op_item`: `OPAbstractItem`
    The edited version of the item

**Service account support**: supported

## Field Editing Operations

There are three categories of field-editing operations:

- Setting a value on an existing field
  - Including changing a field's type. E.g., from "text" to "URL"
- Adding a new field, and optionally a section
- Deleting a field

In all cases, an `item get` operation is first peformed in order to validate the presense or absence of the field being edited. There are different sets of restrictions depending on whether a field is being added, an existing field being assigned a new value, or a field is being deleted. Those restrictions are dicussed below.

### Existing Field Value Setting

If an existing field is being assigned a new value, the original item is retrieved and checked that the requested (field, seciton) pairing exist. Any of the following conditions are considered an error:
- A field with the specified label is not found
- If provided, a section with the specified label is not found
- No section is specified, and no matching fields are found that *have no* associated section

***

`OP.item_edit_set_password()`

Assign a new password for an existing item

**SECURITY NOTE**: This operation will include the provided password in cleartext as a command line argument to the 'op' command. On most platforms, the arguments, including the password, will be visible to other processes, including processes owned by other users. In order to use this operaton, this insecurity must be acknowledged by passing the `insecure_operation=True` kwarg.

**Parameters**

`item_identifier`: `str`
    The item to edit
`password`: `str`
    The password value to set
`field_label`: `str`
    The human readable label of the field to edit
    by default "password"
`section_label`: `str`, optional
    If provided, the human readable section label the field is associated with
`insecure_operation`: `bool`
    Caller acknowledgement of the insecure nature of this operation
    by default, False
`vault`: `str`, optional
    The name or ID of a vault containing the item to edit
    Overrides the OP object's default vault, if set

**Exceptions Raised**

`OPItemGetException`
    If the item lookup fails for any reason
`OPSectionNotFoundException`
    If a section label is specified but can't be looked up on the item object
`OPFieldNotFoundException`
    If the field label can't be looked up on the item object
`OPItemEditException`
    If the item edit operation fails for any reason
`OPInsecureOperationException`
    If the caller does not pass insecure_operation=True, failing to acknowledge the
    insecure nature of this operation

**Returns**

`op_item`: `OPAbstractItem`
    The edited version of the item

**Note**: an 'item_get()` operation first is performed in order to validate
      the field name and, if provided, section name

**Service account support**: supported, required keyword arguments: vault

***

`OP.item_edit_set_text_field()`

Set a new value on an existing item's text field

**Parameters**

`item_identifier`: `str`
    The item to edit
`value`: `str`
    The text value to set
`field_label`: `str`
    The human readable label of the field to edit
`section_label`: `str`, optional
    If provided, the human readable section label the field is associated with
`vault`: `str`, optional
    The name or ID of a vault containing the item to edit
    Overrides the OP object's default vault, if set
`password_downgrade`: `bool`
    Whether and existing concealed (i.e., password) field should be downgraded to a non-password
    field.
    If the existing field IS concealed and this value is false, an exception will be raised

**Exceptions Raised**

`OPItemGetException`
    If the item lookup fails for any reason
`OPSectionNotFoundException`
    If a section label is specified but can't be looked up on the item object
`OPFieldNotFoundException`
    If the field label can't be looked up on the item object
`OPPasswordFieldDowngradeException`
    If the field is a concealed field and password_downgrade is False
`OPItemEditException`
    If the item edit operation fails for any reason

**Returns**

`op_item`: `OPAbstractItem`
    The edited version of the item

**Note**: an 'item_get()` operation first is performed in order to validate
      the field name and, if provided, section name

**Service account support**: supported, required keyword arguments: vault

***

`OP.item_edit_set_url_field()`

Set a new value on an existing item's URL field

**NOTE**: This method differs from item_edit_url(). This method sets a URL value on an existing item field whereas item_edit_url() sets the URL property, which is not a field at all, on a login item

**Parameters**

`item_identifier`: `str`
    The item to edit
`url`: `str`
    The URL value to set
`field_label`: `str`
    The human readable label of the field to edit
`section_label`: `str`, optional
    If provided, the human readable section label the field is associated with
`vault`: `str`, optional
    The name or ID of a vault containing the item to edit
    Overrides the OP object's default vault, if set
`password_downgrade`: `bool`
    Whether and existing concealed (i.e., password) field should be downgraded to a non-password
    field.
    If the existing field IS concealed and this value is false, an exception will be raised

**Exceptions Raised**

`OPItemGetException`
    If the item lookup fails for any reason
`OPSectionNotFoundException`
    If a section label is specified but can't be looked up on the item object
`OPFieldNotFoundException`
    If the field label can't be looked up on the item object
`OPPasswordFieldDowngradeException`
    If the field is a concealed field and password_downgrade is False
`OPItemEditException`
    If the item edit operation fails for any reason

**Returns**

`op_item`: `OPAbstractItem`
    The edited version of the item

**Service account support**: supported, required keyword arguments: vault

**NOTE**: Neither 1Password nor pyonepassword perform any validation on the URLstring. It may be virtually any string.

***

### Adding New Fields

If a new field is being added, the original item is retrieved and checked that the requested field/section pairing *do not* exist. Any of the following conditions are considered an error:
- Ambiguous match:
  - one or more fields match the field label and no section label was specified
- Explicit match:
  - one or more field/section pairings exist that match the field label & section label

`OP.item_edit_add_text_field()`

Add new text field and optionally a new section to an item

**Parameters**

`item_identifier`: `str`
    The item to edit
`value`: `str`
    The text value to set
`field_label`: `str`
    The human readable label of the field to create
`section_label`: `str`, optional
    If provided, the human readable section label the field is associated with.
    It will be created if it doesn't exist
`vault`: `str`, optional
    The name or ID of a vault containing the item to edit
    Overrides the OP object's default vault, if set

**Exceptions Raised**

`OPItemGetException`
    If the item lookup fails for any reason
`OPFieldExistsException`
    If the field to be added already existss
`OPItemEditException`
    If the item edit operation fails for any reason

**Returns**

`op_item`: `OPAbstractItem`
    The edited version of the item

**Service account support**: supported, required keyword arguments: vault

***

`OP.item_edit_add_password_field()`

Add new concealed/passwrod field and optionally a new section to an item

**Parameters**

`item_identifier`: `str`
    The item to edit
`value`: `str`
    The password value to set
`field_label`: `str`
    The human readable label of the field to create
`section_label`: `str`, optional
    If provided, the human readable section label the field is associated with.
    It will be created if it doesn't exist
`vault`: `str`, optional
    The name or ID of a vault containing the item to edit
    Overrides the OP object's default vault, if set

**Exceptions Raised**

`OPItemGetException`
    If the item lookup fails for any reason
`OPFieldExistsException`
    If the field to be added already existss
`OPItemEditException`
    If the item edit operation fails for any reason

**Returns**

`op_item`: `OPAbstractItem`
    The edited version of the item

**Service account support**: supported, required keyword arguments: vault

***

### Deleting Fields

When deleting a field, if the field is associated with a section, and the section has no remaining fields, the section will also be deleted.

Deleting fields has the same restrictions as setting values on existing fields. The original item is retrieved and checked that the requested (field, seciton) pairing exist. Any of the following conditions are considered an error:
- A field with the specified label is not found
- If provided, a section with the specified label is not found
- No section is specified, and no matching fields are found that *have no* associated section


`OP.item_edit_delete_field()`

Delete a field, and optionally a section from an item

If a section is specified, and it has no remaining fields after
the edit operation, the section will be removed as well

**Parameters**

`item_identifier`: `str`
    The item to edit
`field_label`: `str`
    The human readable label of the field to delete
`section_label`: `str`, optional
    If provided, the human readable section label the field is associated with
`vault`: `str`, optional
    The name or ID of a vault containing the item to edit
    Overrides the OP object's default vault, if set

**Exceptions Raised**

`OPItemGetException`
    If the item lookup fails for any reason
`OPSectionNotFoundException`
    If a section label is specified but can't be looked up on the item object
`OPFieldNotFoundException`
    If the field label can't be looked up on the item object
`OPItemEditException`
    If the item edit operation fails for any reason

**Returns**

`op_item`: `OPAbstractItem`
    The edited version of the item

**Service account support**: supported, required keyword arguments: vault
