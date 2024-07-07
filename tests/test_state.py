# test_state.py
import pytest
import torch

from bandit.object import Object
from bandit.state import State, StateBuffer, TemporalState


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


def test_initial_state():
    ts = TemporalState(state_buffer_size=5)
    assert len(ts) == 0
    with pytest.raises(IndexError):
        ts()


def test_add_state():
    ts = TemporalState(state_buffer_size=5)
    state = State(cycle=1, tep=1, root_id=1, temporal_id=1)
    ts._add(state)
    assert len(ts) == 1
    assert ts() == state


#! NOT IMPLEMENTED
# def test_traverse_forward():
#     ts = TemporalState(state_buffer_size=5)
#     state1 = State(cycle=1, tep=1, root_id=1, temporal_id=1)
#     state2 = State(cycle=2, tep=2, root_id=2, temporal_id=2)
#     ts._add(state1)
#     ts._add(state2)

#     ts.traverse_backward()
#     assert ts() == state1
#     ts.traverse_forward()
#     assert ts() == state2
#     with pytest.raises(IndexError):
#         ts.traverse_forward()

#! NOT IMPLEMENTED
# def test_traverse_backward():
#     ts = TemporalState(state_buffer_size=5)
#     state1 = State(cycle=1, tep=1, root_id=1, temporal_id=1)
#     state2 = State(cycle=2, tep=2, root_id=2, temporal_id=2)
#     ts._add(state1)
#     ts._add(state2)

#     assert ts() == state2
#     ts.traverse_backward()
#     assert ts() == state1
#     with pytest.raises(IndexError):
#         ts.traverse_backward()


def test_traverse_empty_buffer():
    ts = TemporalState(state_buffer_size=5)
    with pytest.raises(IndexError):
        ts.traverse_forward()
    with pytest.raises(IndexError):
        ts.traverse_backward()


def test_update_state():
    class MockObject:
        class Clock:
            cycle = 1
            step = 1

        class ID:
            root = 1
            temporal = 1

        clock = Clock()
        id = ID()

    ts = TemporalState(state_buffer_size=5)
    mock_object = MockObject()
    state = ts.update(mock_object)
    assert len(ts) == 1
    assert ts() == state


def test_buffer_wraparound():
    ts = TemporalState(state_buffer_size=2)
    state1 = State(cycle=1, tep=1, root_id=1, temporal_id=1)
    state2 = State(cycle=2, tep=2, root_id=2, temporal_id=2)
    state3 = State(cycle=3, tep=3, root_id=3, temporal_id=3)
    ts._add(state1)
    ts._add(state2)
    ts._add(state3)
    assert len(ts) == 2
    assert ts() == state3
