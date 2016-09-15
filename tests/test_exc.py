from unittest import TestCase

from adventure.exc import AdventureException, UnknownGenderError


class AdventureExceptionTestCase(TestCase):
    def test_inheritance(self):
        self.assertIsInstance(AdventureException(), Exception)
