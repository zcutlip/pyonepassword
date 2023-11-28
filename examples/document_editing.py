from pathlib import Path

from pyonepassword import OP


def replace_document():
    op = OP()
    document_title = "example document 01"
    replacement_file_path = "path/to/replacement_image_01.png"

    op.document_edit(document_title, replacement_file_path)

    # or replacmenet document can be bytes instead of str/Path:
    replacement_bytes = open(replacement_file_path, "rb").read()

    op.document_edit(document_title, replacement_bytes)


def replace_document_set_title():
    op = OP()
    document_title = "example document 01"
    replacement_file_path = "path/to/replacement_image_01.png"
    new_document_title = "updated example document 01"
    op.document_edit(document_title, replacement_file_path,
                     new_title=new_document_title)


def replace_document_set_filename():
    op = OP()
    document_title = "example document 01"

    # replacement path may be Path or str
    replacement_file_path = Path("path/to/replacement_image_01.png")

    # get basename: "replacement_image_01.png"
    new_document_filename = replacement_file_path.name
    op.document_edit(document_title, replacement_file_path,
                     file_name=new_document_filename)
