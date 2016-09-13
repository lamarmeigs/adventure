from unittest import TestCase

from adventure.models import Item


class ItemTestCase(TestCase):
    pass


class InitTestCase(ItemTestCase):
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


class UseTestCase(ItemTestCase):
    pass
