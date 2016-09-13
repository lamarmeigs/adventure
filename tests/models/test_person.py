from unittest import TestCase

from adventure.exc import UnknownGenderError
from adventure.models import Person


class PersonTestCase(TestCase):
    pass


class InitTestCase(PersonTestCase):
    def test_set_parameters(self):
        person = Person(
            name='Gandalf',
            description='An old man dressed in grey',
            gender='male',
            synonym_names=['Mithrandir', 'Stormcrow', 'wizard']
        )
        self.assertEqual(person.name, 'Gandalf')
        self.assertEqual(person.description, 'An old man dressed in grey')
        self.assertEqual(person.gender, 'male')
        self.assertEqual(
            person.synonym_names,
            ['Mithrandir', 'Stormcrow', 'wizard']
        )

    def test_default_parameters(self):
        person = Person(
            name='Hamlet',
            description='Dressed all in black, carrying a skull',
            gender='male'
        )
        self.assertEqual(person.synonym_names, [])


class GenderPropertyTestCase(PersonTestCase):
    def setUp(self):
        super().setUp()
        self.person = Person('Francis', 'Some person', 'male')

    def test_get_property_value(self):
        self.person._gender = 'unknown'
        self.assertEqual(self.person.gender, 'unknown')

    def test_set_property_value(self):
        self.person.gender = 'unspecified'
        self.assertEqual(self.person._gender, 'unspecified')

    def test_unknown_gender_raises_error(self):
        with self.assertRaises(UnknownGenderError) as ctx:
            self.person.gender = 'dinosaur'
        self.assertIn('person "Francis"', str(ctx.exception))
        self.assertIn(str(self.person._allowed_genders), str(ctx.exception))


class PronounPropertiesTestCase(PersonTestCase):
    def setUp(self):
        super().setUp()
        self.person = Person(
            name='Ada Lovelace',
            description='Most badass programmer ever',
            gender='female'
        )

    def test_get_subject_pronoun(self):
        self.assertEqual(
            self.person.subject_pronoun,
            Person._pronouns.get(self.person.gender)['subject']
        )

    def test_get_object_pronoun(self):
        self.assertEqual(
            self.person.object_pronoun,
            Person._pronouns.get(self.person.gender)['object']
        )

    def test_get_possessive_pronoun(self):
        self.assertEqual(
            self.person.possessive_pronoun,
            Person._pronouns.get(self.person.gender)['possessive']
        )


class TalkTestCase(PersonTestCase):
    pass
