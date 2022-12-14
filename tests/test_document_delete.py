# __future__.annotations, and typing.TYPE_CHECKING
# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.exceptions import OPDocumentDeleteException

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from pyonepassword import OP

    from .fixtures.expected_document_data import ExpectedDocumentData

from .test_support.util import digest

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_document_delete_01(signed_in_op: OP, expected_document_data: ExpectedDocumentData):
    """
    Test deleting a document based on its non-unique title
    """
    document_name = "delete this document"
    vault = "Test Data"
    expected = expected_document_data.data_for_document(document_name)
    expected_document_id = expected.item_id
    result = signed_in_op.document_delete(document_name, vault=vault)
    assert result == expected_document_id


def test_document_delete_02(signed_in_op: OP, expected_document_data: ExpectedDocumentData):
    """
    Test deleting and archiving a document based on its non-unique title
    """
    document_name = "delete and archive this document"
    vault = "Test Data"
    expected = expected_document_data.data_for_document(document_name)
    expected_item_id = expected.item_id
    result = signed_in_op.document_delete(
        document_name, vault=vault, archive=True)
    assert result == expected_item_id


def test_document_delete_03(signed_in_op: OP, expected_document_data: ExpectedDocumentData):
    """
    Test:
      - deleting and archiving a document based on its non-unique title
      - fetching the item with include_archive=True
    """
    document_name = "delete and archive this document"
    vault = "Test Data"
    expected = expected_document_data.data_for_document(document_name)

    signed_in_op.document_delete(
        document_name, vault=vault, archive=True)
    filename, data = signed_in_op.document_get(
        document_name, vault=vault, include_archive=True)
    sha256_digest = digest(data)

    assert filename == expected.filename
    assert len(data) == expected.size
    assert sha256_digest == expected.digest


def test_document_delete_non_existent_01(signed_in_op: OP):
    """
    Test deleting a non-existent document
    """
    document_name = "non-existent-item"
    vault = "Test Data"

    with pytest.raises(OPDocumentDeleteException):
        signed_in_op.document_delete(document_name, vault=vault)


def test_document_delete_non_existent_02(signed_in_op: OP):
    """
    Test deleting a non-existent item, bypassing item_get()
    """
    document_name = "non-existent-item"
    vault = "Test Data"

    with pytest.raises(OPDocumentDeleteException):
        # OP.document_delete() calls item_get() first
        # which will fail on non-existent items
        # so in order to test delete operatation failing, we
        # need to call private ._document_delete() interface
        signed_in_op._document_delete(document_name, vault=vault)


def test_document_delete_duplicate_01(signed_in_op: OP):
    """
    Test:
      - deleting a document based on its non-unique title
      - when there are two or more documents sharing the same title
    """
    document_name = "delete this duplicate document"
    vault = "Test Data"

    with pytest.raises(OPDocumentDeleteException):
        signed_in_op.document_delete(document_name, vault=vault)
