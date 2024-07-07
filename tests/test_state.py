# test_state.py
import pytest
import torch

from bandit.object import Object
from bandit.state import State, StateBuffer


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


# StateBuffer Tests
def test_state_buffer():
    state_buffer = StateBuffer(3)
    state_buffer.append("State 1")
    state_buffer.append("State 2")
    state_buffer.append("State 3")
    assert state_buffer[0] == "State 3"
    assert state_buffer[1] == "State 2"
    assert state_buffer[2] == "State 1"
    assert state_buffer[-1] == "State 2"
    assert state_buffer[-2] == "State 1"


def test_state_buffer_get_last_n_states():
    state_buffer = StateBuffer(3)
    state_buffer.append("State 1")
    state_buffer.append("State 2")
    state_buffer.append("State 3")
    assert state_buffer.get_last_n_states(2) == ["State 2", "State 3"]


def test_state_buffer_get_state_at_index():
    state_buffer = StateBuffer(3)
    state_buffer.append("State 1")
    state_buffer.append("State 2")
    state_buffer.append("State 3")
    assert state_buffer.get_state_at_index(0) == "State 3"
    assert state_buffer.get_state_at_index(1) == "State 2"
    assert state_buffer.get_state_at_index(2) == "State 1"
