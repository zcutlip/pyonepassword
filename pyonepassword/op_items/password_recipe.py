class OPInvalidPasswordRecipeException(Exception):
    pass


class OPPasswordRecipe:
    """
    Class for generating an 'op' password recipe string

    From 'op' help text:

    You can customize the password with a password recipe. Specify the
    password length and which character types to use in a comma-separated
    list. Ingredients are:

    - 'letters' for uppercase and lowercase letters
    - 'digits' for numbers
    - 'symbols' for special characters ('!@.-_*')
    - '1' - '64' for password length

    """
    MIN_PASSWD_LEN = 1
    MAX_PASSWD_LEN = 64

    def __init__(self, length: int = 20, letters=True, digits=True, symbols=True):
        """
        Create a OPPasswordRecipe object for passing to the 'op' command for password generation

        Parameters
        ----------
        length : int, optional
            Length of the password to generate, by default 20
        letters : bool, optional
            generated password should include letters, by default True
        digits : bool, optional
            generated password should include digits, by default True
        symbols : bool, optional
            generated password should include symbols, by default True

        Raises
        ------
        OPInvalidPasswordRecipeException
            If:
              - The specified length is outside the range (1-64) accepted by the 'op' command
              - If at least one of letters, digits, or symbols is not requested
        """
        if length < self.MIN_PASSWD_LEN or length > self.MAX_PASSWD_LEN:
            raise OPInvalidPasswordRecipeException(
                f"Invalid password length: {length}")

        recipe_parts = [str(length)]

        if True not in [letters, digits, symbols]:
            raise OPInvalidPasswordRecipeException(
                "Letters, digits, & symbols all disabled. One or more must be enabled")

        if letters:
            recipe_parts.append("letters")
        if digits:
            recipe_parts.append("digits")
        if symbols:
            recipe_parts.append("symbols")

        self.recipe = recipe_parts

    def __str__(self) -> str:
        recipe_str = ",".join(self.recipe)
        return recipe_str

    @classmethod
    def from_string(cls, password_recipe: str):
        """
        Class method for transforming a password recipe string into a OPPasswordRecipe object

        Primarily for validating password recipe strings

        Parameters
        ----------
        password_recipe : str
            The password recipe string to parse and validate

        Raises
        ------
        OPInvalidPasswordRecipeException
            If:
              - The recipe contains a component not recognized by 'op'
              - The recipe is not valid per OPPasswordRecipe's initializer (see constructor docstring)
        """
        letters = False
        digits = False
        symbols = False

        parts = password_recipe.split(",")

        # password length will be validated in __init__()
        try:
            passwd_len = int(parts.pop(0))
        except ValueError:
            raise OPInvalidPasswordRecipeException(
                "Recipe must start with password length in the range 1-64")

        for part in parts:
            if part == "letters":
                letters = True
            elif part == "digits":
                digits = True
            elif part == "symbols":
                symbols = True
            else:
                raise OPInvalidPasswordRecipeException(
                    f"Invalid password recipe component: {part}")
        recipe = cls(length=passwd_len, letters=letters,
                     digits=digits, symbols=symbols)
        return recipe


LETTERS_DIGITS_SYMBOLS_20 = OPPasswordRecipe()
LETTERS_DIGITS_25 = OPPasswordRecipe(length=25, symbols=False)
