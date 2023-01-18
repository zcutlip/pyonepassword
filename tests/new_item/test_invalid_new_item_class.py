import pytest

from pyonepassword.api.exceptions import OPInvalidItemException
from pyonepassword.op_items._new_item import OPNewItemMixin


class OPInvalidLoginItemTemplate(OPNewItemMixin):
    def __init__(self, title: str, fields=[], sections=[], extra_data={}):
        super().__init__(title, fields, sections, extra_data)


def test_invalid_new_item_class_01():

    with pytest.raises(OPInvalidItemException):
        OPNewItemMixin("invalid-new-item")


def test_invalid_login_item_template_01():
    with pytest.raises(OPInvalidItemException):
        OPInvalidLoginItemTemplate("invalid login item template")
