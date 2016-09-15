import json
import os
from unittest import TestCase

from adventure.fixtures import load_fixture


class DummyModel:
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar


class LoadFixtureTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_path = 'test_fixture.json'
        cls.fixtures = [{'foo': 5, 'bar': 6}, {'foo': 1, 'bar': 2}]
        with open(cls.file_path, 'w') as test_file:
            test_file.write(json.dumps(cls.fixtures))

    def test_loads_objects(self):
        dummies = load_fixture(self.file_path, DummyModel)
        self.assertEqual(len(dummies), len(self.fixtures))
        self.assertEqual(dummies[0].foo, self.fixtures[0]['foo'])
        self.assertEqual(dummies[0].bar, self.fixtures[0]['bar'])
        self.assertEqual(dummies[1].foo, self.fixtures[1]['foo'])
        self.assertEqual(dummies[1].bar, self.fixtures[1]['bar'])

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.file_path)
