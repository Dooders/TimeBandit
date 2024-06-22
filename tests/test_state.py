# test_state.py
import pytest
import torch

from bandit.state import State, StateBuffer, TemporalState


# State Tests
def test_state():
    state = State({"a": 1, "b": 2})
    assert state["a"] == 1
    assert state["b"] == 2


def test_state_encode():
    pass


def test_state_decode():
    pass


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


# TemporalState Tests
def test_temporal_state():
    temporal_state = TemporalState(3)
    temporal_state.add("State 1")
    temporal_state.add("State 2")
    temporal_state.add("State 3")
    assert temporal_state[0] == "State 3"
    assert temporal_state[1] == "State 2"
    assert temporal_state[2] == "State 1"
    assert temporal_state() == "State 3"
