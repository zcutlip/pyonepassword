import pytest

from pyonepassword.api.object_types import OPPasswordRecipe
from pyonepassword.op_items.password_recipe import (
    OPInvalidPasswordRecipeException
)


def test_password_recipe_010():
    """
    Create a password recipe with:
        - custom length
        - letters, digits, & symbols explicitly True
    Verify:
        the resulting recipe matches the expected recipe
    """
    expected_recipe = "25,letters,digits,symbols"
    length = 25
    letters = True
    digits = True
    symbols = True
    recipe = OPPasswordRecipe(
        length=length, letters=letters, digits=digits, symbols=symbols)
    assert expected_recipe == str(recipe)


def test_password_recipe_020():
    """
    Create a password recipe with:
        - custom length
        - letters, digits explicitly True
        - symbols explicitly False
    Verify:
        the resulting recipe matches the expected recipe
    """
    expected_recipe = "30,letters,digits"
    length = 30
    letters = True
    digits = True
    symbols = False
    recipe = OPPasswordRecipe(
        length=length, letters=letters, digits=digits, symbols=symbols)
    assert expected_recipe == str(recipe)


def test_password_recipe_030():
    """
    Create a password recipe with:
        - custom length
        - letters explicitlyh False
        - digits, symbols explicitly True
    Verify:
        the resulting recipe matches the expected recipe
    """
    expected_recipe = "50,digits,symbols"
    length = 50
    letters = False
    digits = True
    symbols = True
    recipe = OPPasswordRecipe(
        length=length, letters=letters, digits=digits, symbols=symbols)
    assert expected_recipe == str(recipe)


def test_password_recipe_040():
    """
    Create a password recipe with all default values
    Verify:
        the resulting recipe matches the expected recipe
    """
    expected_recipe = "20,letters,digits,symbols"

    recipe = OPPasswordRecipe()
    assert expected_recipe == str(recipe)


def test_password_recipe_050():
    """
    Create a password recipe with:
        - custom length
        - default values for letters, digits, & symbols
    Verify:
        the resulting recipe matches the expected recipe
    """
    expected_recipe = "36,letters,digits,symbols"
    length = 36
    recipe = OPPasswordRecipe(length=length)
    assert expected_recipe == str(recipe)


def test_password_recipe_exception_060():
    """
    Create a password recipe with:
        - letters, digits, & symbols explicitly False
    Verify:
        OPInvalidPasswordRecipeException is raised
    """
    letters = False
    digits = False
    symbols = False
    with pytest.raises(OPInvalidPasswordRecipeException):
        OPPasswordRecipe(letters=letters, digits=digits, symbols=symbols)
