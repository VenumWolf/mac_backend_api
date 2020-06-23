from unittest import TestCase

from mac_backend_api.utils.random_ids.random_id import random_id


class TestRandomIdGenerator(TestCase):

    def test_random_id(self):
        """Ensures default length is met"""
        assert len(random_id()) == 14

    def test_random_id_custom_character_set_as_string(self):
        """Ensures custom character sets are honored when tye are passed as a string"""
        character_set = "1234"
        generated_id = random_id(4, character_set)
        self.__assert_only_valid_characters(generated_id, character_set)

    def test_random_id_custom_character_set_as_list(self):
        """Ensures custom character sets are honored when they are passed as a list"""
        character_set = ['1', '2', '3', '4']
        generated_id = random_id(4, character_set)
        self.__assert_only_valid_characters(generated_id, character_set)

    def test_random_id_custom_character_set_as_tuple(self):
        """Ensures custom character sets are honored when they are passed as a tuple"""
        character_set = ('1', '2', '3', '4')
        generated_id = random_id(4, character_set)
        self.__assert_only_valid_characters(generated_id, character_set)

    def test_random_id_with_empty_character_set(self):
        """Ensures the character set may not be empty"""
        self.assertRaises(ValueError, random_id, character_set=list())

    def test_random_id_with_length_0(self):
        """Ensures length value may not be 0"""
        self.assertRaises(ValueError, random_id, length=0)

    def test_random_id_with_negative_length(self):
        """Ensures length value may not be less than 0"""
        self.assertRaises(ValueError, random_id, length=-10)

    def test_random_id_for_duplicates(self):
        """Ensures returned values are randomized"""
        for i in range(100):
            first_id = random_id()
            second_id = random_id()
            assert first_id != second_id

    def __assert_only_valid_characters(self, characters, character_set):
        """Assert if a set of characters match a given character_set"""
        for character in characters:
            assert character in character_set
