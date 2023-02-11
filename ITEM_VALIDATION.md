# Item Object Validation

When instantiating 'item' objects, `pyonepassword` attempts to validate the well-formedness of the item dictionary, and raise meaningful exceptions to the caller if non-conformant data is encountered.


## Well Formed Items

What "well-formed" means for an item dictionary isn't really documented, but there are a few things that appear to be consistently true, and make sense intuitively:

**fields**
Fields in 1Password items should, at a minimum, conform to the following rules

- Every field has an "id" element
- The the field IDs should be unique across all the fields in a given item
- A field may optionally be associated with at most one section

**sections**
Similarly to fields, sections should conform to the following rules

- Every section has an "id" element
- The section IDs should be unique across all sections in a given item
- A section may not be associated with a field which is associated to another section


## Exceptions

When instantiating an item object from a dictionary, if the above rules are violated, one of the following sections will be raised:

- `OPSectionCollsionException`: if multiple sections are present with the same ID
- `OPItemFieldCollisionException`: if multiple fields are present with the same ID
- `OPInvalidItemException`: If a field or section is present with no ID at all

## Relaxed Item Validation Policy

It has been observed that the `op` command occasionally returns item dictionaries that don't conform to the above rules. This is most likely to happen in 1Password accounts that pre-date existence of the `op` command and items have been created by number of different versions of the 1Password app.

In such cases, it is possible to relax validation, and use `pyonepassword` as normal. The relaxed validation API makes this possible. Here are the details of this API

**`OP` query methods**

The item query methods of the op class all have an optional `relaxed_validation` kwarg that defaults to `False`. For example you can query an item object, enabling relaxed validation for that one request like so;

```python
op = OP()
non_conformant_item = op.item_get("Example Login", relaxed_validation=True)
```

Future queries will not have relaxed validaiton unless the caller continues to pass `relaxed_validation=True`.

The following methods on `OP` objects all have this optional kwarg:

- `OP.item_get()`
- `OP.item_get_password()`
- `OP.item_get_filename()`
- `OP.item_delete()`
- `OP.document_get()`
- `OP.document_delete()`

**Item Validation Policy API**

In addition to a query-by-query bases, item validaiton policy can be adjusted globally. There are methods to enable, disable, and query item validaiton policy either for a specific item type, or for all items.

> *NOTE*: Even if item validation is relaxed global for one or even all item types, strict validation policy still applies when creating new 1Password items from template, such as `OPLoginItemTemplate`.


The following functions, found in `pyonepassword.api.validation`, are available to set & query item validaiton policy for individual or for all classes globally:

**All Classes Global Policy**:

- `enable_relaxed_validation()`: Set relaxed item validation for all item types, globally
- `disable_relaxed_validation()`: Disable relaxed item validation for all item types, globally
- `get_relaxed_validation(item_class=None)`: Query relaxed item validation policy
  - If `item_class` is provided, the result is a union like so: (`global_relaxed` or `class_relaxed`)
  - This is to say the answer is `True` if either relaxed validaiton is enabled for all classes or just the one class


**Per-class Global Policy**

- `set_relaxed_validation_for_class(item_class)`: Enable relaxed item validation for `item_class`
  - May be called mutiple times to relax validation for more than one item class
- `set_strict_validation_for_class(item_class)`: Remove `item_class` from the relaxed validation list
  - *NOTE*: If relaxed validation is enabled for all classes is enabled, it takes precedent
- `get_relaxed_validation_for_class(item_class)`: Query whether `item_class` has is in the relaxed validation class list
  - *NOTE*: The result does not consider the global all-class relaxed validation policy
