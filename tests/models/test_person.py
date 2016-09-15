from unittest import TestCase
from unittest.mock import patch

from adventure.models import Person, Gender


class GenderTestCase(TestCase):
    def test_init_sets_attributes(self):
        unspecified = Gender('unspecified', 'they', 'them', 'their')
        self.assertEqual(unspecified.gender, 'unspecified')
        self.assertEqual(unspecified.subject_pronoun, 'they')
        self.assertEqual(unspecified.object_pronoun, 'them')
        self.assertEqual(unspecified.possessive_pronoun, 'their')

    def test_init_calls_super_with_identifier(self):
        with patch('adventure.models.base.BaseModel.__init__') as mock_init:
            Gender('female', 'she', 'her', 'her', _identifier=1)
        mock_init.assert_called_once_with(_identifier=1)

    def test_serialize(self):
        judy = Gender('judy', 'judy', 'judy', "judy's")
        self.assertEqual(
            judy.serialize(),
            {
                'gender': judy.gender,
                'subject_pronoun': judy.subject_pronoun,
                'object_pronoun': judy.object_pronoun,
                'possessive_pronoun': judy.possessive_pronoun,
                '_identifier': judy._identifier,
            }
        )

    def test_str(self):
        male = Gender('male', 'he', 'him', 'his', _identifier=5)
        self.assertEqual(str(male), '<Gender 5: male>')


class PersonTestCase(TestCase):
    def setUp(self):
        self.gender = Gender('unspecified', 'they', 'them', 'their')

    def test_talk(self):
        pass

    def test_serialize(self):
        person = Person('Jane', 'A real Mensch', self.gender, ['mensch'])
        serialized_person = person.serialize()
        self.assertEqual(
            serialized_person,
            {
                'name': person.name,
                'description': person.description,
                'gender': person.gender.reference,
                'synonym_names': person.synonym_names,
                '_identifier': person._identifier,
            }
        )

    def test_str(self):
        person = Person(
            name='Willy Wonka',
            description='Purple suit and all',
            gender=self.gender,
            _identifier=18
        )
        self.assertEqual(str(person), '<Person 18: Willy Wonka>')


class PersonInitTestCase(TestCase):
    def setUp(self):
        self.male_gender = Gender('male', 'he', 'him', 'his')

    def test_set_parameters(self):
        person = Person(
            name='Gandalf',
            description='An old man dressed in grey',
            gender=self.male_gender,
            synonym_names=['Mithrandir', 'Stormcrow', 'wizard', 'old man']
        )
        self.assertEqual(person.name, 'Gandalf')
        self.assertEqual(person.description, 'An old man dressed in grey')
        self.assertEqual(person.gender, self.male_gender)
        self.assertEqual(
            person.synonym_names,
            ['Mithrandir', 'Stormcrow', 'wizard', 'old man']
        )

    def test_default_parameters(self):
        person = Person(
            name='Hamlet',
            description='Dressed all in black, carrying a skull',
            gender=self.male_gender,
        )
        self.assertEqual(person.synonym_names, [])

    def test_call_super_with_identifier(self):
        with patch('adventure.models.base.BaseModel.__init__') as mock_init:
            Person(
                name='Blackbeard',
                description="His beard's on fire!",
                gender=self.male_gender,
                _identifier=3
            )
        mock_init.assert_called_once_with(_identifier=3)
