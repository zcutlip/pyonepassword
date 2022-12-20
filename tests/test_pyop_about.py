from pyonepassword import OP


def _about_string():
    from pyonepassword.__about__ import __summary__, __title__, __version__
    about_str = f"{__title__.upper()}: {__summary__}. Version {__version__}"
    return about_str


def test_pyop_about_01():
    about_str = _about_string()
    assert OP.about() == about_str


def test_pyop_version_01():
    from pyonepassword.__about__ import __version__
    assert OP.version() == __version__
