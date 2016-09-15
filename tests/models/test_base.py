from unittest import TestCase

from adventure.models.base import BaseModel, SerializedReference


class BaseModelTestCase(TestCase):
    def test_serialize_raises_not_implemented_error(self):
        class DummyModel(BaseModel):
            def serialize(self):
                super().serialize()

        dummy = DummyModel()
        with self.assertRaises(NotImplementedError):
            dummy.serialize()


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


class SerializedReferenceTestCase(TestCase):
    def test_init_sets_keys(self):
        ref = SerializedReference('foo.bar.baz', '42')
        self.assertEqual(ref, {'model_ref': 'foo.bar.baz', 'identifier': '42'})

    def test_str(self):
        ref = SerializedReference('path.to.class', '77')
        self.assertEqual(str(ref), '<SerializedReference: path.to.class 77>')
