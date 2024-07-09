# test_state.py
import pytest
import torch

from bandit.object import Object
from bandit.state import State


class MockObject(Object):
    def __init__(self):
        super().__init__()

    def _update(self):
        pass


# State Tests
def test_state():
    state = State({"a": 1, "b": 2})
    assert state["a"] == 1
    assert state["b"] == 2


def test_state_encode():
    """
    Test the encode method of the State class.
    Unimplemented for now.
    """
    pass


def test_state_decode():
    """
    Test the decode method of the State class.
    Unimplemented for now.
    """
    pass


# State tests
def test_state_flatten():
    state = State({"a": 1, "b": 2})
    assert state._flatten() == [1, 2]


def test_state_tensor():
    state = State({"a": 1, "b": 2})
    assert torch.equal(state.tensor(), torch.tensor([1.0, 2.0], dtype=torch.float32))
