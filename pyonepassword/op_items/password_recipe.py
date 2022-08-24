class OPInvalidPasswordRecipeException(Exception):
    pass


class OPPasswordRecipe:
    def __init__(self, length: int = 20, letters=True, digits=True, symbols=True):
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


LETTERS_DIGITS_SYMBOLS_20 = OPPasswordRecipe()
LETTERS_DIGITS_25 = OPPasswordRecipe(length=25, symbols=False)
