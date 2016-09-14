from unittest import TestCase

from adventure.models.base import BaseModel


class BaseModelTestCase(TestCase):
    pass


class InitTestCase(BaseModelTestCase):
    def test_count_incremented(self):
        class DummyModelA(BaseModel):
            def serialize(self):
                pass

        class DummyModelB(BaseModel):
            def serialize(self):
                pass

        dummy_1 = DummyModelA()
        self.assertEqual(BaseModel.COUNT, 0)
        self.assertEqual(DummyModelA.COUNT, 1)
        self.assertEqual(DummyModelB.COUNT, 0)
        self.assertEqual(dummy_1._identifier, 1)


class SerializeTestCase(BaseModelTestCase):
    def test_raise_not_implemented_error(self):
        class DummyModelC(BaseModel):
            def serialize(self):
                super().serialize()

        dummy = DummyModelC()
        with self.assertRaises(NotImplementedError):
            dummy.serialize()
