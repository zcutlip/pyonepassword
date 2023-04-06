# __future__.annotaitons, and typing.TYPE_CHECKING
# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from typing import TYPE_CHECKING

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from ..fixtures.expected_server import ExpectedServerItemData
    from ..fixtures.valid_data import ValidData

from pyonepassword.api.object_types import OPServerItem


def test_server_item_010(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    """
    Create:
        - OPServerItem object from example-server-1 input data
    Verify:
        - username property matches expected value
    """
    server_name = "Example Server"

    item_dict = valid_data.data_for_name("example-server-1")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)
    assert result.username == expected.username


def test_server_item_020(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    """
    Create:
        - OPServerItem object from example-server-1 input data
    Verify:
        - password property matches expected value
    """
    server_name = "Example Server"

    item_dict = valid_data.data_for_name("example-server-1")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)
    assert result.password == expected.password


def test_server_item_030(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    """
    Create:
        - OPServerItem object from example-server-1 input data
    Verify:
        - url property matches expected value
    """

    server_name = "Example Server"
    item_dict = valid_data.data_for_name("example-server-1")
    expected = expected_server_data.data_for_server(server_name)
    result = OPServerItem(item_dict)
    assert result.url == expected.url


def test_server_item_040(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    """
    Create:
        - OPServerItem object from example-server-2 input data
    Verify:
        - url property matches expected value
    """
    server_name = "Example Server 2"

    item_dict = valid_data.data_for_name("example-server-2")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)
    assert result.url == expected.url


def test_server_item_050(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    """
    Create:
        - OPServerItem object from example-server-2 input data
    Verify:
        - admin_console_username property matches expected value
    """
    server_name = "Example Server 2"

    item_dict = valid_data.data_for_name("example-server-2")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)
    assert result.admin_console_username == expected.admin_console_username


def test_server_item_060(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    """
    Create:
        - OPServerItem object from example-server-2 input data
    Verify:
        - admin_console_password property matches expected value
    """
    server_name = "Example Server 2"

    item_dict = valid_data.data_for_name("example-server-2")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)
    assert result.admin_console_password == expected.admin_console_password


def test_server_item_070(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    """
    Create:
        - OPServerItem object from example-server-1 input data
    Verify:
        - hosting_provider_name property matches expected value
    """
    server_name = "Example Server"

    item_dict = valid_data.data_for_name("example-server-1")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)

    assert result.hosting_provider_name == expected.hosting_provider_name


def test_server_item_080(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    """
    Create:
        - OPServerItem object from example-server-1 input data
    Verify:
        - hosting_provider_website property matches expected value
    """
    server_name = "Example Server"

    item_dict = valid_data.data_for_name("example-server-1")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)

    assert result.hosting_provider_website == expected.hosting_provider_website


def test_server_item_090(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    """
    Create:
        - OPServerItem object from example-server-1 input data
    Verify:
        - support_contact_url property matches expected value
    """
    server_name = "Example Server"

    item_dict = valid_data.data_for_name("example-server-1")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)

    assert result.support_contact_url == expected.support_contact_url


def test_server_item_100(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    """
    Create:
        - OPServerItem object from example-server-1 input data
    Verify:
        - support_contact_phone property matches expected value
    """
    server_name = "Example Server"

    item_dict = valid_data.data_for_name("example-server-1")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)

    assert result.support_contact_phone == expected.support_contact_phone
