from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyonepassword import OP

import pytest

from pyonepassword.api.exceptions import (
    OPDocumentGetException,
    OPInvalidDocumentException
)
from pyonepassword.api.object_types import OPDocumentFile, OPDocumentItem

from .test_support.util import digest

pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_document_get01(signed_in_op: OP, expected_document_data):
    item_name = "Example Login 2 - 1200px-SpongeBob_SquarePants_character.svg.png.webp"
    vault = "Test Data"
    expected = expected_document_data.data_for_document(item_name)
    filename, data = signed_in_op.document_get(item_name, vault=vault)
    sha256_digest = digest(data)
    assert filename == expected.filename
    assert len(data) == expected.size
    assert sha256_digest == expected.digest


@pytest.mark.parametrize("invalid_document,vault",
                         [("Invalid Document", None),
                          ("Error Success", "Test Data"),
                          ("Example Attached File 2", None)])
def test_document_get02(signed_in_op: OP, expected_document_data, invalid_document, vault):
    exception_class = OPDocumentGetException
    expected = expected_document_data.data_for_document(invalid_document)
    try:
        signed_in_op.document_get(invalid_document, vault=vault)
        assert False, f"We should have caught {exception_class.__name__}"
    except exception_class as e:
        assert expected.returncode == e.returncode


def test_document_get03(signed_in_op: OP, expected_document_data):
    item_name = "Example Login 2 - 1200px-SpongeBob_SquarePants_character.svg.png.webp"
    vault = "Test Data"
    expected: OPDocumentItem = expected_document_data.data_for_document(
        item_name)
    document_item = signed_in_op.item_get(item_name, vault=vault)
    assert isinstance(document_item, OPDocumentItem)
    document_files = document_item.files
    file_obj = document_files[0]
    assert isinstance(file_obj, OPDocumentFile)
    assert file_obj.size == expected.size
    assert file_obj.content_path == expected.content_path
    assert file_obj.file_id == expected.file_id


def test_document_get_wrong_item_type_01(signed_in_op: OP):
    with pytest.raises(OPInvalidDocumentException):
        signed_in_op.document_get("Not A Document")
