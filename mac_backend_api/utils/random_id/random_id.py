import string
from random import SystemRandom

URLSAFE_SPECIALS = "-._~"

DEFAULT_ID_LENGTH = 14
DEFAULT_CHARACTER_SET = string.ascii_letters + string.digits + URLSAFE_SPECIALS


def random_id(length=DEFAULT_ID_LENGTH, character_set=DEFAULT_CHARACTER_SET):
    """
    Generate a random ID with the given length and character_set.
    :param length:        The length of the id
    :param character_set: A string, list, or a tuple containing the characters from which to create the ID
    :return:              A random ID of the given length and character set
    """
    if length < 1: raise ValueError("Length must be at least 1")
    if len(character_set) < 1: raise ValueError("The character set is empty")
    characters = list()
    for character in range(length):
        characters.append(SystemRandom().choice(character_set))
    return "".join(characters)
