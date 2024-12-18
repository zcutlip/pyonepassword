from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyonepassword.api.object_types import OPPasswordRecipe

if TYPE_CHECKING:
    from pyonepassword import OP
    from pyonepassword.api.object_types import OPLoginItem

    from ....fixtures.expected_login import (
        ExpectedLogin,
        ExpectedLoginItemData
    )

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _get_item_password(item: OPLoginItem, field_label: str = "password", section_label: str = None):
    section = None
    if section_label:
        section = item.first_section_by_label(section_label)

    if section:
        field = section.first_field_by_label(field_label)
    else:
        field = item.first_field_by_label(field_label)

    password = field.value
    return password


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_password_010(signed_in_op: OP):
    """
    Test: OP.item_edit_set_password()
        - Retrieve an item via OP.item_get()
        - Call item_edit_set_password(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's password is not equal to the desired new password
        - The returned edited item's password is the same as newly retrieved item's password
        - The newly retrieved item's password is the same as the desired new password

    """

    item_name = "Example Login Item 00"
    field_label = "password"
    new_password = "new password"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    assert item_get_1.password != new_password

    edited_item = signed_in_op.item_edit_set_password(item_name,
                                                      new_password,
                                                      field_label=field_label,
                                                      insecure_operation=True,
                                                      vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    assert edited_item.password == item_get_2.password
    assert item_get_2.password == new_password


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_set_password_015(signed_in_op: OP):
    """
    Test: OP.item_edit_set_password()
        - Retrieve an item via OP.item_get()
        - Call item_edit_set_password(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's password is not equal to the desired new password
        - The returned edited item's password is the same as newly retrieved item's password
        - The newly retrieved item's password is the same as the desired new password

    """

    item_name = "Example Login Item 03"
    section_label = "Example Section"
    field_label = "password in a section"
    new_password = "new password in a section"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    item_get_password_1 = _get_item_password(
        item_get_1, field_label=field_label, section_label=section_label)

    assert item_get_password_1 != new_password

    edited_item = signed_in_op.item_edit_set_password(item_name,
                                                      new_password,
                                                      field_label=field_label,
                                                      section_label=section_label,
                                                      insecure_operation=True,
                                                      vault=vault)

    edited_item_password = _get_item_password(
        edited_item, field_label=field_label, section_label=section_label)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)
    item_get_password_2 = _get_item_password(
        item_get_2, field_label=field_label, section_label=section_label)

    assert edited_item_password == item_get_password_2
    assert item_get_password_2 == new_password


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_gen_password_020(signed_in_op: OP,
                                    expected_login_item_data: ExpectedLoginItemData):
    """
    Test: OP.item_edit_generate_password()
        - Retrieve an item via OP.item_get()
        - Call item_edit_generate_password(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's password matches the expected original password
        - The returned edited item's password is not the same as the original item's password
        - The newly retrieved item's password matches the expected edited item's password
    """
    item_name = "Example Login Item 01"
    vault = "Test Data 2"

    password_recipe = OPPasswordRecipe(20, symbols=False)

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    expected_item_original: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name)
    expected_item_edited: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name, version=1)
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    assert item_get_1.password == expected_item_original.password

    edited_item = signed_in_op.item_edit_generate_password(item_name,
                                                           password_recipe,
                                                           vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    assert edited_item.password != item_get_1.password
    assert item_get_2.password == expected_item_edited.password


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_title_030(signed_in_op: OP):
    """
    Test: OP.item_edit_title()
        - Retrieve an item via OP.item_get() using the original title
        - Call item_edit_title(), saving returned object
        - Retreive the same item a second time using the new title

    Verify:
        - The original item's password matches the expected original password
        - The returned edited item's password is not the same as the original item's password
        - The newly retrieved item's password matches the expected edited item's password
    """
    item_name = "Example Login Item 02"
    item_name_new = "Example Login Item 02 (New Title)"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    # sort of obvious since we retrieved using the old title, but for the sake of completeness
    assert item_get_1.title != item_name_new
    edited_item = signed_in_op.item_edit_title(
        item_name, item_name_new, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name_new, vault=vault)

    assert edited_item.title == item_get_2.title
    assert item_get_2.title == item_name_new


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_favorite_040(signed_in_op: OP):
    """
    Test: OP.item_edit_favorite() setting favorite to True
        - Retrieve an item via OP.item_get()
        - Call item_edit_favorite(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's favorite flag is False
        - The returned edited item's favorite flag matches the newly retrieved item's favorite flag
        - The newly retrieved item's favorite flag is True
    """
    item_name = "Example Login Item 04"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    assert item_get_1.favorite is False

    edited_item = signed_in_op.item_edit_favorite(
        item_name, True, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    assert edited_item.favorite == item_get_2.favorite
    assert item_get_2.favorite is True


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_favorite_050(signed_in_op: OP):
    """
    Test: OP.item_edit_favorite() setting favorite to False
        - Retrieve an item via OP.item_get()
        - Call item_edit_favorite(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's favorite flag is True
        - The returned edited item's favorite flag matches the newly retrieved item's favorite flag
        - The newly retrieved item's favorite flag is False
    """
    item_name = "Example Login Item 05"
    vault = "Test Data 2"

    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    assert item_get_1.favorite is True

    edited_item = signed_in_op.item_edit_favorite(
        item_name, False, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    assert edited_item.favorite == item_get_2.favorite
    assert item_get_2.favorite is False


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_tags_060(signed_in_op: OP):
    """
    Test: OP.item_edit_tags() to replace an items set of tags with a different set of tags
        - Retrieve an item via OP.item_get()
        - Call item_edit_tags(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's tags match the expected original set of tags
        - The returned edited item's tags match the newly retrieved item's set of tags
        - The newly retrieved item's set of tags match the expected new set of tags
    """
    item_name = "Example Login Item 06"
    vault = "Test Data 2"
    original_tag_set = {"tag_1", "tag_2"}

    new_tags = ["tag_3", "tag_4", "tag_5"]
    new_tag_set = set(new_tags)
    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    assert set(item_get_1.tags) == original_tag_set

    edited_item = signed_in_op.item_edit_tags(
        item_name, new_tags, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    assert set(edited_item.tags) == set(item_get_2.tags)
    assert set(item_get_2.tags) == new_tag_set


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_tags_070(signed_in_op: OP):
    """
    Test: OP.item_edit_tags() to set tags on an item with no existing tags
        - Retrieve an item via OP.item_get()
        - Call item_edit_tags(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's set of tags is empty
        - The returned edited item's tags match the newly retrieved item's set of tags
        - The newly retrieved item's set of tags match the expected new set of tags
    """
    item_name = "Example Login Item 07"
    vault = "Test Data 2"
    original_tag_set = set([])

    new_tags = ["tag_1", "tag_2", "tag_3"]
    new_tag_set = set(new_tags)
    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    assert set(item_get_1.tags) == original_tag_set

    edited_item = signed_in_op.item_edit_tags(
        item_name, new_tags, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    assert set(edited_item.tags) == set(item_get_2.tags)
    assert set(item_get_2.tags) == new_tag_set


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_tags_080(signed_in_op: OP):
    """
    Test: OP.item_edit_tags() to remove tags on an item that already has tags
        - Retrieve an item via OP.item_get()
        - Call item_edit_tags(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's set of tags is empty
        - The returned edited item's tags match the newly retrieved item's set of tags
        - The newly retrieved item's set of tags match the expected new set of tags
    """
    item_name = "Example Login Item 08"
    vault = "Test Data 2"

    original_tag_set = set(["tag_1", "tag_2", "tag_3"])
    new_tags = set([])
    new_tag_set = set(new_tags)
    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    assert set(item_get_1.tags) == original_tag_set

    edited_item = signed_in_op.item_edit_tags(
        item_name, new_tags, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    assert set(edited_item.tags) == set(item_get_2.tags)
    assert set(item_get_2.tags) == new_tag_set


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_tags_085(signed_in_op: OP):
    """
    Test: OP.item_edit_tags() append tags to an item's existing set of tags
        - Retrieve an item via OP.item_get()
        - Call item_edit_tags(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item's set of tags match the expected original set of tags
        - The returned edited item's tags match the newly retrieved item's set of tags
        - The newly retrieved item's set of tags match the expected combined set of tags
    """
    item_name = "Example Login Item 08a"
    vault = "Test Data 2"

    original_tag_set = set(["tag_1", "tag_2", "tag_3"])
    new_tags = ["tag_3", "tag_4", "tag_5"]

    # set of unique tags from original and new set
    new_tag_set = set(["tag_1", "tag_2", "tag_3"] + new_tags)
    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1 = signed_in_op.item_get(item_name, vault=vault)

    assert set(item_get_1.tags) == original_tag_set

    edited_item = signed_in_op.item_edit_tags(
        item_name, new_tags, append_tags=True, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2 = signed_in_op.item_get(item_name, vault=vault)

    assert set(edited_item.tags) == set(item_get_2.tags)
    assert set(item_get_2.tags) == new_tag_set


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_url_090(signed_in_op: OP):
    """
    Test: OP.item_edit_url() to set an item's URL
        - Retrieve an item via OP.item_get()
        - Call item_edit_url(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item has no URLs set
        - The returned edited item has the same number of URLs as the newly retrieved item
        - The newly retrieved item's primary URL's href matches the new URL
    """
    item_name = "Example Login Item 09"
    vault = "Test Data 2"

    new_url = "https://item-09-url.com/login.html"
    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1: OPLoginItem = signed_in_op.item_get(item_name, vault=vault)

    # sort of obvious since we retrieved using the old title, but for the sake of completeness
    assert len(item_get_1.urls) == 0

    edited_item: OPLoginItem = signed_in_op.item_edit_url(
        item_name, new_url, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2: OPLoginItem = signed_in_op.item_get(item_name, vault=vault)

    assert len(edited_item.urls) == len(item_get_2.urls)
    assert len(item_get_2.urls) == 1
    assert item_get_2.primary_url.href == new_url


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_url_100(signed_in_op: OP):
    """
    Test: OP.item_edit_url() to set an item's URL
        - Retrieve an item via OP.item_get()
        - Call item_edit_url(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item has 1 URL set
        - The returned edited item has the same number of URLs as the newly retrieved item
        - The newly retrieved item's primary URL's href matches the new URL
    """
    item_name = "Example Login Item 10"
    vault = "Test Data 2"

    new_url = "https://item-10-url.com/login.html"
    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1: OPLoginItem = signed_in_op.item_get(item_name, vault=vault)

    # sort of obvious since we retrieved using the old title, but for the sake of completeness
    assert len(item_get_1.urls) == 1

    edited_item: OPLoginItem = signed_in_op.item_edit_url(
        item_name, new_url, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2: OPLoginItem = signed_in_op.item_get(item_name, vault=vault)

    assert len(edited_item.urls) == len(item_get_2.urls)
    assert len(item_get_2.urls) == 1
    assert item_get_2.primary_url.href == new_url


@pytest.mark.usefixtures("setup_stateful_item_edit")
def test_item_edit_url_110(signed_in_op: OP):
    """
    Test: OP.item_edit_url() to set an item's URL
        - Retrieve an item via OP.item_get()
        - Call item_edit_url(), saving returned object
        - Retreive the same item a second time

    Verify:
        - The original item has 2 URLs set
        - The returned edited item has the same number of URLs as the newly retrieved item
        - The newly retrieved item continues to have 2 URLs set
        - The newly retrieved item's primary URL's href matches the new URL
    """
    item_name = "Example Login Item 11"
    vault = "Test Data 2"

    new_url = "https://item-11-url.com/login.html"
    # stateful response directory
    # state 1: responses-item-edit/response-directory-1.json
    item_get_1: OPLoginItem = signed_in_op.item_get(item_name, vault=vault)

    # sort of obvious since we retrieved using the old title, but for the sake of completeness
    assert len(item_get_1.urls) == 2

    edited_item: OPLoginItem = signed_in_op.item_edit_url(
        item_name, new_url, vault=vault)

    # state changed with item_edit above
    # state 2: responses-item-edit/response-directory-2.json
    item_get_2: OPLoginItem = signed_in_op.item_get(item_name, vault=vault)

    assert len(edited_item.urls) == len(item_get_2.urls)
    assert len(item_get_2.urls) == 2
    assert item_get_2.primary_url.href == new_url
