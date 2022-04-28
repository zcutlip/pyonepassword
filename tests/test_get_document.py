from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyonepassword import OP

import pytest

from pyonepassword import OPGetDocumentException
from .test_support.util import digest


def test_get_document_01(signed_in_op: OP, expected_document_data):
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
def test_get_document_02(signed_in_op: OP, expected_document_data, invalid_document, vault):
    exception_class = OPGetDocumentException
    expected = expected_document_data.data_for_document(invalid_document)
    try:
        signed_in_op.document_get(invalid_document, vault=vault)
        assert False, f"We should have caught {exception_class.__name__}"
    except exception_class as e:
        assert expected.returncode == e.returncode
