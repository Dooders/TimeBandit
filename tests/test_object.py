import unittest
from unittest.mock import Mock, patch

from bandit.clock import Clock
from bandit.object import Object


class TestObject(unittest.TestCase):

    def setUp(self):
        self.obj = Object()

    def test_initialization(self):
        self.assertEqual(self.obj.steps_size, 1)
        self.assertIsInstance(self.obj.root_id, str)
        self.assertEqual(len(self.obj.root_id), 32)
        self.assertIsInstance(self.obj.temporal_id, str)

    def test_str_representation(self):
        self.assertEqual(str(self.obj), f"Object:{self.obj.root_id}")

    def test_repr_representation(self):
        self.assertEqual(repr(self.obj), f"Object:{self.obj.root_id}")

    def test_update(self):
        with patch.object(Clock, "update") as mock_update:
            self.obj.update()
            mock_update.assert_called_once()
        self.assertEqual(self.obj.state["cycle"], self.obj.clock.cycle)
        self.assertEqual(self.obj.state["step"], self.obj.clock.step)

    def test_encode(self):
        expected_encoding = (
            f"{self.obj.root_id}.{self.obj.clock.cycle}.{self.obj.clock.step}"
        )
        self.assertEqual(self.obj.encode(), expected_encoding)

    def test_id_method(self):
        self.assertEqual(self.obj.id(), self.obj.temporal_id)
        self.assertEqual(self.obj.id(root=True), self.obj.root_id)

    def test_state_property(self):
        state = self.obj.state
        self.assertEqual(state["cycle"], self.obj.clock.cycle)
        self.assertEqual(state["step"], self.obj.clock.step)
        self.assertEqual(state["root_id"], self.obj.root_id)
        self.assertEqual(state["temporal_id"], self.obj.temporal_id)

    def test_cycle_property(self):
        self.assertEqual(self.obj.cycle, self.obj.clock.cycle)

    def test_step_property(self):
        self.assertEqual(self.obj.step, self.obj.clock.step)


if __name__ == "__main__":
    unittest.main()
