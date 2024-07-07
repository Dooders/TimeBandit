import os
import unittest
from unittest.mock import patch

from bandit.clock import Clock
from bandit.object import Object


class MockObject(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _update(self):
        pass


class TestObject(unittest.TestCase):

    def setUp(self):
        self.obj = MockObject()

    def test_initialization(self):
        self.assertEqual(self.obj.steps_size, 1)
        self.assertIsInstance(self.obj.id.root, str)
        self.assertEqual(len(self.obj.id.root), 32)
        self.assertIsInstance(self.obj.id.temporal, str)

    def test_str_representation(self):
        self.assertEqual(str(self.obj), f"MockObject:{self.obj.id.root}")

    def test_repr_representation(self):
        self.assertEqual(repr(self.obj), f"MockObject:{self.obj.id.root}")

    @patch.object(MockObject, "_update")
    def test_update(self, mock_update):
        self.obj.update()
        mock_update.assert_called_once()

    def test_id(self):
        self.assertEqual(self.obj.id(), self.obj.id.temporal)
        self.assertEqual(self.obj.id(root=True), self.obj.id.root)

    def test_save(self):
        path = self.obj.save(".")
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    def test_load(self):
        path = self.obj.save(".")
        obj = self.obj.load(path)
        self.assertEqual(obj.id.root, self.obj.id.root)
        self.assertEqual(obj.id.temporal, self.obj.id.temporal)
        os.remove(path)

    def test_state_property(self):
        state = self.obj.state()
        self.assertEqual(state["cycle"], self.obj.clock.cycle)
        self.assertEqual(state["step"], self.obj.clock.step)
        self.assertEqual(state["root_id"], self.obj.id.root)
        self.assertEqual(state["temporal_id"], self.obj.id.temporal)

    def test_cycle_property(self):
        self.assertEqual(self.obj.cycle, self.obj.clock.cycle)

    def test_step_property(self):
        self.assertEqual(self.obj.step, self.obj.clock.step)
