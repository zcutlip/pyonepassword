class RedactableString(str):
    """
    A string subclass that automatically self-redacts when printed, logged or cast to a str()

    When interacted with directly, it behaves as a typical string
    """
    # how much to leave unmasked at the end
    UNMASK_LEN = 5

    _orig_string: str
    _redacted_string: str

    def __new__(cls, string):
        orig_string = string
        if isinstance(string, cls):
            orig_string = string._orig_string
        obj = str.__new__(cls, orig_string)
        obj._orig_string = orig_string
        obj._redacted_string = cls._redacted(orig_string)
        return obj

    def __str__(self):
        return self._redacted_string

    def __iadd__(self, other):
        # since strings are immutable,
        # when you call mystr += "extra"
        # the string isn't modified
        # you actually get a new string object
        # so we can make this work just by calling __add__()
        return self.__add__(other)

    def __add__(self, other):
        if isinstance(other, RedactableString):
            other = other._orig_string
        new_str = RedactableString(self._orig_string + other)
        return new_str

    @property
    def original(self) -> str:
        return self._orig_string

    @classmethod
    def _redacted(cls, orig_string) -> str:
        # This aims to turn:
        # 5GHHPJK5HZC5BAT7WDUXW57G44 into
        # *********************57G44

        if len(orig_string) <= cls.UNMASK_LEN:
            # the thing is too short, so replace everything
            orig_string = "*" * len(orig_string)
        else:
            # get the length of the portion we're trying to mask
            star_count = len(orig_string) - cls.UNMASK_LEN

            # make the star mask
            stars = "*" * star_count
            # get the bit we want to leave unmasked
            _last_five = orig_string[-(cls.UNMASK_LEN):]

            # join the mask with the end part we're leaving unmasked
            orig_string = stars + _last_five
        return orig_string
