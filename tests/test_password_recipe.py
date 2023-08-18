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


def test_password_recipe_exception_070():
    """
    Create a password recipe with:
        - Length value less than the minimum of 1
    Verify:
        OPInvalidPasswordRecipeException is raised
    """
    length = 0
    with pytest.raises(OPInvalidPasswordRecipeException):
        OPPasswordRecipe(length=length)


def test_password_recipe_exception_080():
    """
    Create a password recipe with:
        - Length value greater than the maximum 64
    Verify:
        OPInvalidPasswordRecipeException is raised
    """
    length = 65
    with pytest.raises(OPInvalidPasswordRecipeException):
        OPPasswordRecipe(length=length)


def test_password_recipe_exception_090():
    """
    Create a password recipe with:
        - Negative length value
    Verify:
        OPInvalidPasswordRecipeException is raised
    """
    length = -127
    with pytest.raises(OPInvalidPasswordRecipeException):
        OPPasswordRecipe(length=length)


def test_password_recipe_from_string_100():
    """
    Create a password recipe using from_string(), with:
        - Custom length greater than the maximum 64
        - letters, digits, & symbols
    Verify:
        the resulting recipe matches the expected recipe
    """

    input_string = "64,letters,digits,symbols"
    expected_recipe = "64,letters,digits,symbols"

    recipe = OPPasswordRecipe.from_string(input_string)

    assert expected_recipe == str(recipe)


def test_password_recipe_from_string_110():
    """
    Create a password recipe using from_string(), with:
        - custom length
        - letters & digits
    Verify:
        the resulting recipe matches the expected recipe
    """

    input_string = "20,letters,digits"
    expected_recipe = "20,letters,digits"

    recipe = OPPasswordRecipe.from_string(input_string)

    assert expected_recipe == str(recipe)


def test_password_recipe_from_string_120():
    """
    Create a password recipe using from_string(), with:
        - Custom length larger the maximum
        - letters, digits, & symbols
    Verify:
        the resulting recipe matches the expected recipe
    """

    input_string = "65,letters,digits"

    with pytest.raises(OPInvalidPasswordRecipeException):
        OPPasswordRecipe.from_string(input_string)


def test_password_recipe_from_string_130():
    """
    Create a password recipe using from_string(), with:
        - Omitted length, only letters & digits specified
    Verify:
        OPInvalidPasswordRecipeException is raised
    """
    input_string = "letters,digits"

    with pytest.raises(OPInvalidPasswordRecipeException):
        OPPasswordRecipe.from_string(input_string)


def test_password_recipe_from_string_140():
    """
    Create a password recipe using from_string(), with:
        - an illegal string consisting of emojis
    Verify:
        OPInvalidPasswordRecipeException is raised
    """
    input_string = "🍆🍆🍆"

    with pytest.raises(OPInvalidPasswordRecipeException):
        OPPasswordRecipe.from_string(input_string)


def test_password_recipe_from_string_150():
    """
    Create a password recipe using from_string(), with:
        - an illegal string consisting of length, letters, digits, and an emoji
    Verify:
        OPInvalidPasswordRecipeException is raised
    """
    input_string = "25,letters,digits,🙃"

    with pytest.raises(OPInvalidPasswordRecipeException):
        OPPasswordRecipe.from_string(input_string)
