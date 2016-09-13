from unittest import TestCase

from adventure.exc import AdventureException, UnknownGenderError


class AdventureExceptionTestCase(TestCase):
    def test_inheritance(self):
        self.assertIsInstance(AdventureException(), Exception)


class UnknownGenderErrorTestCase(TestCase):
    def test_inheritance(self):
        self.assertIsInstance(UnknownGenderError('foo'), AdventureException)

    def test_simple_message(self):
        error = UnknownGenderError('tree')
        self.assertEqual(str(error), 'Unknown gender "tree" found')

    def test_complex_message(self):
        error = UnknownGenderError(
            'bird',
            context='person Birdman',
            allowed_genders=['unspecified']
        )
        self.assertEqual(
            str(error),
            'Unknown gender "bird" found in person Birdman. Expected gender '
            "to be one of ['unspecified']"
        )
