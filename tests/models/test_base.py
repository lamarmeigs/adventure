from unittest import TestCase
from unittest.mock import patch

from adventure.models.base import BaseModel, SerializedReference


class BaseModelTestCase(TestCase):
    def test_serialize_raises_not_implemented_error(self):
        class DummyModel(BaseModel):
            def serialize(self):
                super().serialize()

        dummy = DummyModel()
        with self.assertRaises(NotImplementedError):
            dummy.serialize()

    def test_reference(self):
        class RefModel(BaseModel):
            def serialize(self):
                pass

        dummy = RefModel()
        self.assertEqual(
            dummy.reference,
            SerializedReference('tests.models.test_base.RefModel', 1)
        )

    def test_str(self):
        class StrModel(BaseModel):
            def serialize(self):
                pass

        dummy = StrModel(_identifier=2)
        self.assertEqual(str(dummy), '<StrModel 2>')

    def test_repr(self):
        class ReprModel(BaseModel):
            def serialize(self):
                pass

        dummy = ReprModel(_identifier=9)
        with patch.object(dummy, '__str__', return_value='repr') as mock_str:
            dummy_repr = dummy.__repr__()
        mock_str.assert_called_once_with()
        self.assertEqual(dummy_repr, 'repr')


class BaseModelInitTestCase(TestCase):
    def test_increments_subclass_count(self):
        class DummyModelA(BaseModel):
            def serialize(self):
                pass

        class DummyModelB(BaseModel):
            def serialize(self):
                pass

        dummy_a = DummyModelA()
        self.assertEqual(BaseModel.COUNT, 0)
        self.assertEqual(DummyModelA.COUNT, 1)
        self.assertEqual(DummyModelB.COUNT, 0)
        self.assertEqual(dummy_a._identifier, 1)

    def test_sets_identifier(self):
        class DummyModelC(BaseModel):
            def serialize(self):
                pass

        dummy_1 = DummyModelC(_identifier=5)
        self.assertEqual(dummy_1._identifier, 5)
        self.assertEqual(DummyModelC.COUNT, 5)

        dummy_2 = DummyModelC(_identifier=2)
        self.assertEqual(dummy_2._identifier, 2)
        self.assertEqual(DummyModelC.COUNT, 5)


class BaseModelEquivalenceTestCase(TestCase):
    class EqualityModel(BaseModel):
        def serialize(self):
            pass

    class OtherEqualityModel(BaseModel):
        def serialize(self):
            pass

    def test_full_eq(self):
        dummy_1 = self.EqualityModel(_identifier=4)
        dummy_2 = self.EqualityModel(_identifier=4)
        self.assertTrue(dummy_1.__eq__(dummy_2))
        self.assertTrue(dummy_2.__eq__(dummy_1))

    def test_differing_classes(self):
        dummy_1 = self.EqualityModel(_identifier=7)
        dummy_2 = self.OtherEqualityModel(_identifier=7)
        self.assertFalse(dummy_1.__eq__(dummy_2))
        self.assertFalse(dummy_2.__eq__(dummy_1))

    def test_differing_identifiers(self):
        dummy_1 = self.EqualityModel(_identifier=4)
        dummy_2 = self.EqualityModel(_identifier=7)
        self.assertFalse(dummy_1.__eq__(dummy_2))
        self.assertFalse(dummy_2.__eq__(dummy_1))

    def test_neq_returns_opposite_of_eq(self):
        dummy_1 = self.EqualityModel(_identifier=4)
        dummy_2 = self.EqualityModel(_identifier=4)
        with patch.object(dummy_1, '__eq__', return_value=True):
            self.assertFalse(dummy_1.__neq__(dummy_2))
        with patch.object(dummy_1, '__eq__', return_value=False):
            self.assertTrue(dummy_1.__neq__(dummy_2))


class SerializedReferenceTestCase(TestCase):
    def test_init_sets_keys(self):
        ref = SerializedReference('foo.bar.baz', '42')
        self.assertEqual(ref, {'model_ref': 'foo.bar.baz', 'identifier': '42'})

    def test_str(self):
        ref = SerializedReference('path.to.class', '77')
        self.assertEqual(str(ref), '<SerializedReference: path.to.class 77>')
