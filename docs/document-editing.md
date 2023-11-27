# PYONEPASSWORD DOCUMENT EDITING

## Description
As of version 4.1.0, `pyonepassword` supports in-place document editing. There is API to match the operations supported by the `op document edit` command.

The API for document editing is the `OP.docuemnt_edit()` method. This method replaces the bytes of an existing document item with the contents of a new file.


## Use and arguments
The `document_edit()` method takes two mandatory arguments:

- `document_identitifer`: A string representing the title or unique ID of a document item
- `file_path_or_document_bytes`: This is what the document should be replaced with. It may be either:
  - A `str` or `Path` object referencing existing file on disk to read
  - A `bytes` object that is the new file's contents

Additionally, you may *also* change the document item's:

  - filename via the `file_name=` kwarg
  - title via the `new_title=` kwarg

**Note**: You may not set a new filename or document item title via document_edit() without also specifying a path or bytes to set the document's contents to. This is not supported by `op document edit`. If this behavior is required, the equivalent would be to provide the original document's contents

### Return value

If successful, the `document_edit()` function returns a string representing the unique ID of the document item edited. This may be useful for confirming the expected document item is the one that was edited, in the event a document title was provided.
