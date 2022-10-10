from pyonepassword.api.object_types import (
    OPLoginItemNewPrimaryURL,
    OPLoginItemNewURL,
    OPNewLoginItem
)


def test_new_login_item_url_01():
    url = "https://example.com/index.html"
    label = "Example URL"

    new_url = OPLoginItemNewURL(url, label)
    assert new_url.href == url


def test_new_login_item_url_02():
    url = "https://example.com/index.html"
    label = "Example URL"

    new_url = OPLoginItemNewURL(url, label)
    assert new_url.label == label


def test_new_login_item_url_03():
    url = "https://example.com/index.html"
    label = "Example URL"

    new_url = OPLoginItemNewURL(url, label)
    assert not new_url.primary


def test_new_login_item_url_04():
    url = "https://example.com/index.html"
    label = "Example URL"

    new_url = OPLoginItemNewURL(url, label, primary=True)
    assert new_url.primary


def test_new_login_item_url_05():
    url = "https://example.com/index.html"
    label = "Example URL"

    new_url = OPLoginItemNewPrimaryURL(url, label)
    assert new_url.primary


def test_new_login_item_01():
    username = "test_username"
    title = "Test Login Item"
    primary_url = "https://example.com/index.html"
    url_label = "Example URL"

    new_url = OPLoginItemNewPrimaryURL(primary_url, url_label)
    new_login = OPNewLoginItem(title, username,  url=new_url)
    assert new_login.username == username


def test_new_login_item_02():
    username = "test_username"
    title = "Test Login Item"
    primary_url = "https://example.com/index.html"
    url_label = "Example URL"

    new_url = OPLoginItemNewPrimaryURL(primary_url, url_label)
    new_login = OPNewLoginItem(title, username,  url=new_url)
    assert new_login.primary_url.href == new_url.href


def test_new_login_item_03():
    username = "test_username"
    title = "Test Login Item"
    primary_url = "https://example.com/index.html"
    primary_url_label = "Example URL"

    second_url = "https://second-example.com"
    second_url_label = "Secondary URL"

    primary_url = OPLoginItemNewPrimaryURL(primary_url, primary_url_label)
    second_url = OPLoginItemNewURL(second_url, second_url_label)

    new_login = OPNewLoginItem(title, username,  url=primary_url)

    new_login.add_url(second_url)
    assert new_login.urls[1].href == second_url.href


def test_new_login_item_04():
    username = "test_username"
    title = "Test Login Item"
    primary_url = "https://example.com/index.html"
    primary_url_label = "Example URL"

    second_url = "https://second-example.com"
    second_url_label = "Secondary URL"

    primary_url = OPLoginItemNewPrimaryURL(primary_url, primary_url_label)
    second_url = OPLoginItemNewURL(second_url, second_url_label)

    new_login = OPNewLoginItem(title, username,  url=primary_url)

    new_login.add_url(second_url)
    assert new_login.primary_url.href == primary_url.href


def test_new_login_item_05():
    username = "test_username"
    title = "Test Login Item"
    primary_url = "https://example.com/index.html"
    primary_url_label = "Example URL"
    primary_url = OPLoginItemNewPrimaryURL(primary_url, primary_url_label)

    new_login = OPNewLoginItem(title, username)

    new_login.add_url(primary_url)
    assert new_login.primary_url.href == primary_url.href
