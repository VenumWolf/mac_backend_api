#  Copyright (C) 2020  Mind Audio Central
#
#  This file is part of mac_backend_api.
#
#  mac_backend_api is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  mac_backend_api is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with mac_backend_api.  If not, see <https://www.gnu.org/licenses/>.

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
