from unittest import TestCase
from unittest.mock import patch

from adventure.exc import UnknownGenderError
from adventure.models import Person


class PersonTestCase(TestCase):
    def test_talk(self):
        pass

    def test_serialize(self):
        person = Person('Jane', 'A real Mensch', 'unspecified', ['mensch'])
        serialized_person = person.serialize()
        self.assertEqual(
            serialized_person,
            {
                'name': person.name,
                'description': person.description,
                'gender': person.gender,
                'synonym_names': person.synonym_names,
                '_identifier': person._identifier,
            }
        )


class PersonInitTestCase(TestCase):
    def test_set_parameters(self):
        person = Person(
            name='Gandalf',
            description='An old man dressed in grey',
            gender='male',
            synonym_names=['Mithrandir', 'Stormcrow', 'wizard', 'old man']
        )
        self.assertEqual(person.name, 'Gandalf')
        self.assertEqual(person.description, 'An old man dressed in grey')
        self.assertEqual(person.gender, 'male')
        self.assertEqual(
            person.synonym_names,
            ['Mithrandir', 'Stormcrow', 'wizard', 'old man']
        )

    def test_default_parameters(self):
        person = Person(
            name='Hamlet',
            description='Dressed all in black, carrying a skull',
            gender='male'
        )
        self.assertEqual(person.synonym_names, [])

    def test_call_super_with_identifier(self):
        with patch('adventure.models.base.BaseModel.__init__') as mock_init:
            Person(
                name='Blackbeard',
                description="His beard's on fire!",
                gender='male',
                _identifier=3
            )
        mock_init.assert_called_once_with(_identifier=3)


class GenderPropertyTestCase(TestCase):
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


class PronounPropertiesTestCase(TestCase):
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
