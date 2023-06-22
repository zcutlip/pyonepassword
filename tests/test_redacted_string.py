from pyonepassword.string import RedactedString


def test_redacted_string_010():
    """
    Create a RedactedString object

    Verify the redacted string matches the expected value
    """
    original_string = "An example, unredacted string"
    expected = "************************tring"

    redacted = RedactedString(original_string)
    assert expected == str(redacted)


def test_redacted_string_020():
    """
    Create a RedactedString object with an arbitrarly long unmask_len

    Verify:
        The unmasked portion of the redacted string is appropriate clamped
        to 20% of the string length
    """
    original_string = "An example, unredacted string"
    expected = "************************tring"

    # the max unmasked length of the above string be clamped to 5
    long_unmask_len = 12

    redacted = RedactedString(original_string, unmask_len=long_unmask_len)
    assert expected == str(redacted)


def test_redacted_string_030():
    """
    Create a RedactedString object with an short unmask_len

    Verify:
        The unmasked portion of the redacted string is appropriate restricted
        to the specified value
    """
    original_string = "at 60 characters. this is an even longer string than normal."
    expected = "*************************************************han normal."

    unmask_len = 11

    redacted = RedactedString(original_string, unmask_len=unmask_len)
    assert expected == str(redacted)


def test_redacted_string_040():
    """
    Create a RedactedString object with an arbitrarly long unmask_len

    Verify:
        The unmasked portion of the redacted string is appropriate clamped
        to 20% of the string length
    """
    original_string = "at 60 characters. this is an even longer string than normal."
    # the max unmasked length of the above string be clamped to 12
    expected = "************************************************than normal."

    long_unmask_len = 17

    redacted = RedactedString(original_string, unmask_len=long_unmask_len)
    assert expected == str(redacted)


def test_redacted_string_050():
    """
    Create a RedactedString object with a negative unmask_len

    Verify:
        The unmasked portion of the redacted string is the default length
    """
    original_string = "at 60 characters. this is an even longer string than normal."
    expected = "*******************************************************rmal."

    # a negative unmask length should result in the default unmask length
    long_unmask_len = -5

    redacted = RedactedString(original_string, unmask_len=long_unmask_len)
    assert expected == str(redacted)


def test_redacted_string_060():
    """
    Create a RedactedString object from a short string

    Verify:
        The entire string is masked
    """
    original_string = "short"

    # a very short string should remain completely masked
    expected = "*****"

    redacted = RedactedString(original_string)
    assert expected == str(redacted)


def test_redacted_string_070():
    """
    Create a RedactedString object from a short string,
        specifying a unmask_len of 20% of the string length

    Verify:
        The unmask_len is ignored, and entire string is masked
    """
    original_string = "short"

    # even when specifying an unmask_len,
    # a very short string should remain completely masked
    expected = "*****"

    unmask_len = 1

    redacted = RedactedString(original_string, unmask_len=unmask_len)
    assert expected == str(redacted)


def test_redacted_string_090():
    """
    Create a RedactedString from an existing RedactedString object

    Verify:
        - The two objects are equal
        - The second redacted value matches the expected value
    """
    original_string = "An example, unredacted string"
    expected = "************************tring"

    r1 = RedactedString(original_string)
    r2 = RedactedString(r1)
    assert expected == str(r2)
    assert r2 == r1


def test_redacted_string_100():
    """
    Create a RedactedString object, and concatenate a second string to it

    Verify the redacted value matches the expected value
    """
    original_string = "An example, unredacted string"

    expected_redacted = "*****************************************onger"

    redacted = RedactedString(original_string)
    redacted += ", now even longer"
    assert expected_redacted == str(redacted)


def test_redacted_string_110():
    """
    Create a RedactedString object, and concatenate a second string to it

    Verify the object is equal to the expected unredacted string
    """
    original_string = "An example, unredacted string"
    expected_original = "An example, unredacted string, now even longer"

    redacted = RedactedString(original_string)
    redacted += ", now even longer"
    assert expected_original == redacted


def test_redacted_string_120():
    """
    Create:
        - a RedactedString object,
        - a second RedactedString object by adding a second string to the first

    Verify the second redacted value matches the expected value
    """
    original_string = "An example, unredacted string"
    expected_redacted = "*****************************************onger"

    r1 = RedactedString(original_string)
    r2 = r1 + ", now even longer"
    assert expected_redacted == str(r2)


def test_redacted_string_130():
    """
    Create:
        - Two RedactedString objects
        - A third RedactedString object by adding the first two together

    Verify the third redacted value matches the expected value
    """
    orig_1 = "Redacted part 1."
    orig_2 = " Redacted part 2."
    expected_redacted = "****************************rt 2."

    r1 = RedactedString(orig_1)
    r2 = RedactedString(orig_2)
    r3 = r1 + r2
    assert expected_redacted == str(r3)


def test_redacted_string_140():
    """
    Create:
        - Two RedactedString objects
        - A third RedactedString object by adding the first two together

    Verify the third's 'original' property matches the expected original
    """
    orig_1 = "Redacted part 1."
    orig_2 = " Redacted part 2."

    expected_original = orig_1 + orig_2

    r1 = RedactedString(orig_1)
    r2 = RedactedString(orig_2)
    r3 = r1 + r2
    assert expected_original == r3.original


def test_redacted_string_150():
    """
    Create:
        - Two RedactedString objects
        - A third RedactedString object by adding the first two together

    Verify an abitrary slice of the third object matches the same arbitrary slice of the original
    """
    orig_1 = "Redacted part 1."
    orig_2 = " Redacted part 2."

    expected_original = orig_1 + orig_2

    r1 = RedactedString(orig_1)
    r2 = RedactedString(orig_2)
    r3 = r1 + r2

    assert expected_original[:5] == r3[:5]
