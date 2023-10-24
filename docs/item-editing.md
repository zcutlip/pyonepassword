# PYONEPASSWORD ITEM EDITING

As of version 4.0.0, `pyonepassword` supports in-place item editing. There is API to match the operations supported by the `op item edit` command. This file describes the API as well as its restrictions and limitations. It is recommended to consult `op item edit --help` for any restrictions in addition those enforced by `pyonepassword` described here.

All of the methods described below are instance method on the `pyonepassword.OP` class.

The supported operations break down into two groups: operations that work with arbitrary item fields (and optionally sections), and ones that do not. The first group described are the non-field editing operations, followed by the field editing operations.


## Non-field Editing Operations

The following item editing methods do not operate on arbitrary sections and fields:

- `OP.item_edit_set_favorite()`
- `OP.item_edit_generate_password()`
- `OP.item_edit_set_title()`
- `OP.item_edit_set_tags()`
- `OP.item_edit_set_url()`

> **Note**: Technically `OP.item_edit_generate_password()` operates on a field, but it only works on the built-in "password" field of Login and Password items.


## Field Editing Operations

There are three categories of field-editing operations:

- Setting a value on an existing field
  - Including changing a field's type. E.g., from "text" to "URL"
- Adding a new field, and optionally a section
- Deleting a field

In all cases, an `item get` operation is first peformed in order to validate the presense or absence of the field being edited. There are different sets of restrictions depending on whether a field is being added, an existing field being assigned a new value, or a field is being deleted. Those restrictions are dicussed below.


### Existing Field Value Setting

If an existing field is being assigned a new value, the original item is retrieved and checked that the requested field/section pairing exist. Any of the following conditions are considered an error:
- A field with the specified label is not found
- If provided, a section with the specified label is not found
- No section is specified, and no matching fields are found that *have no* associated section

If the existing field is a password field, and setting a new value would change it to some other field type, the `password_downgrade=True` kwarg must be passed.

*SECURITY NOTE*: The `OP.item_edit_set_password()` method will include the provided password in cleartext as a command line argument to the `op` command. On most platforms, the arguments, including the password, will be visible to other processes, including processes owned by other users. In order to use this operaton, this insecurity must be acknowledged by passing the `insecure_operation=True` kwarg

The following methods operate on arbitrary fields and sections, provided they already exist:

- `OP.item_edit_set_password()`
- `OP.item_edit_set_text_field()`
- `OP.item_edit_set_url_field()`


### Adding New Fields

If a new field is being added, the original item is retrieved and checked that the requested field/section pairing *do not* exist. Any of the following conditions are considered an error:
- Ambiguous match:
  - one or more fields match the field label and no section label was specified
- Explicit match:
  - one or more field/section pairings exist that match the field label & section label

The following methods will add arbitrary fields and optionally sections, provided they do not already exist:

- `OP.item_edit_add_text_field()`
- `OP.item_edit_add_password_field()`


### Deleting Fields

When deleting a field, if the field is associated with a section, and the section has no remaining fields, the section will also be deleted.

Deleting fields has the same restrictions as setting values on existing fields. The original item is retrieved and checked that the requested (field, seciton) pairing exist. Any of the following conditions are considered an error:
- A field with the specified label is not found
- If provided, a section with the specified label is not found
- No section is specified, and no matching fields are found that *have no* associated section

The following method will delete arbitary fields and optionally sections, provided they already exist:

- `OP.item_edit_delete_field()`
