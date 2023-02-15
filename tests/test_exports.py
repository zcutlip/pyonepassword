import pyonepassword.api.authentication
import pyonepassword.api.constants
import pyonepassword.api.decorators
import pyonepassword.api.descriptor_types
import pyonepassword.api.exceptions
import pyonepassword.api.object_types
import pyonepassword.api.validation

"""
Test that all symbols exported from pyonepassword.api are properly re-exported
"""


def test_authentication_exports():
    """
    Verify all symbols in pyonepassword.api.authentication are properly re-exported
    """
    authentication_all = pyonepassword.api.authentication.__all__
    for symbol in dir(pyonepassword.api.authentication):
        if symbol.startswith("__"):
            continue
        assert symbol in authentication_all


def test_constants_exports():
    """
    Verify all symbols in pyonepassword.api.constants are properly re-exported
    """
    constants_all = pyonepassword.api.constants.__all__
    for symbol in dir(pyonepassword.api.constants):
        if symbol.startswith("__"):
            continue
        assert symbol in constants_all


def test_decorators_exports():
    """
    Verify all symbols in pyonepassword.api.decorators are properly re-exported
    """
    decorators_all = pyonepassword.api.decorators.__all__
    for symbol in dir(pyonepassword.api.decorators):
        if symbol.startswith("__"):
            continue
        assert symbol in decorators_all


def test_descriptor_types_exports():
    """
    Verify all symbols in pyonepassword.api.descriptor_types are properly re-exported
    """
    descriptor_types_all = pyonepassword.api.descriptor_types.__all__
    for symbol in dir(pyonepassword.api.descriptor_types):
        if symbol.startswith("__"):
            continue
        assert symbol in descriptor_types_all


def test_exceptions_exports():
    """
    Verify all symbols in pyonepassword.api.exceptions are properly re-exported
    """
    exceptions_all = pyonepassword.api.exceptions.__all__
    for symbol in dir(pyonepassword.api.exceptions):
        if symbol.startswith("__"):
            continue
        assert symbol in exceptions_all


def test_object_types_exports():
    """
    Verify all symbols in pyonepassword.api.object_types are properly re-exported
    """
    object_types_all = pyonepassword.api.object_types.__all__
    for symbol in dir(pyonepassword.api.object_types):
        if symbol.startswith("__"):
            continue
        assert symbol in object_types_all


def test_object_validation_exports():
    """
    Verify all synmbols in pyonepassword.api.validation are properly re-exported
    """
    assert hasattr(pyonepassword.api.validation, "__all__")
    validation_all = pyonepassword.api.validation.__all__
    for symbol in dir(pyonepassword.api.validation):
        if symbol.startswith("__"):
            continue
        assert symbol in validation_all
