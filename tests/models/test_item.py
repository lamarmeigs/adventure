from unittest import TestCase
from unittest.mock import patch

from adventure.models import Item


class ItemTestCase(TestCase):
    def test_use(self):
        pass

    def test_serialize(self):
        item = Item(
            name='thing',
            synonym_names=['object', 'thingy'],
            description='It looks like a thing',
            is_gettable=True,
        )
        serialized_item = item.serialize()
        self.assertEqual(
            serialized_item,
            {
                'name': item.name,
                'synonym_names': item.synonym_names,
                'description': item.description,
                'is_gettable': item.is_gettable,
                '_identifier': item._identifier,
            }
        )


class ItemInitTestCase(TestCase):
    def test_set_parameters(self):
        item = Item(
            name='box of sand',
            synonym_names=['box', 'sand'],
            description='A large gilded box, full of sand',
            is_gettable=True
        )
        self.assertEqual(item.name, 'box of sand')
        self.assertEqual(item.synonym_names, ['box', 'sand'])
        self.assertEqual(item.description, 'A large gilded box, full of sand')
        self.assertTrue(item.is_gettable)

    def test_default_parameters(self):
        item = Item(name='ball')
        self.assertEqual(item.name, 'ball')
        self.assertEqual(item.synonym_names, [])
        self.assertEqual(item.description, '')
        self.assertFalse(item.is_gettable)

    def test_call_super_with_identifier(self):
        with patch('adventure.models.base.BaseModel.__init__') as mock_init:
            Item(name='sword', _identifier=8)
        mock_init.assert_called_once_with(_identifier=8)
