"""
A temporal state buffer for storing states in a temporal sense.
The buffer is a deque with a maxlen.
The current_index is the index of the current state.


FUTURE PLANS

Encode and Decode Object State through an auto-encoder

Encoding allows compression of the object state into a lower dimensional 
representation that can recombine with genetic algorithms.

The idea is to get the minimal amount of information needed to reinstate the 
object state within a range of error, which serves as a mutation mechanism if 
using evolutionary algorithms.

The object state is everything needed to reinstate the object, which includes
the root id, temporal id, cycle, step, and steps per cycle.

The object state also contains the model parameters of the object, which is what 
influences the object's behavior in the simulation.


# To Do
- Implement the encode and decode methods in the ObjectState class
- Implement the encode_self method in the Object class
- Condense an object state into a single string, and then decode it back to the 
    original state
- This will give the ability to store the state of an object in a database and 
    easily reinstate it

#! Maybe an evolutionary approach to an auto-encoder that slowly compresses the 
#!   encoding more and more, as long as the decoding output is correct
#! Will hopefully need less and less context/information to reinstate the object 
#!   from the encoded data


#! state method that turns the state into a tensor, combine that with space input state tensor, to input into the object update method for "updating"
#! update method must log the update_time attribute of the object
#! so all requests to update come through the State class and it controls the update process of the object(s)
"""

from collections import deque
from typing import Any

import torch


class State(dict):
    """
    A state in the temporal state buffer.
    Extends dict to allow for arbitrary state data.

    Parameters
    ----------
    state : dict
        The state to store.

    Methods
    -------
    encode()
        Encodes the state to another state.
    decode()
        Decodes the state to another state.
    tensor()
        Returns the state as a tensor.
    """

    def __init__(self, state: dict) -> None:
        super().__init__(state)

    def encode(self) -> str:
        """
        Encodes the state to another state.
        """
        raise NotImplementedError("Haven't developed this yet")

    def decode(self) -> dict:
        """
        Decodes the state to another state.
        """
        raise NotImplementedError("Haven't developed this yet")

    def _flatten(self) -> list[float]:
        """
        Flattens the state to a list of floats.
        """
        return [item for sublist in self.values() for item in sublist]

    def tensor(self) -> torch.Tensor:
        """
        Returns the state as a tensor.
        """
        # Take the contents of the dict and flatten to a single tensor
        return torch.tensor(self._flatten(), dtype=torch.float32)


class StateBuffer:
    """
    A buffer for storing states in a temporal sense.
    The buffer is a deque with a maxlen.
    The current_index is the index of the current state.

    Parameters
    ----------
    size : int
        The maximum number of states to store.

    Methods
    -------
    append(data)
        Appends a state to the buffer.
    get_last_n_states(n)
        Returns the last n states from the buffer.
    get_state_at_index(index)
        Returns the state at the given index.
    move_forward(n=1)
        Moves the current index forward by n steps.
    move_backward(n=1)
        Moves the current index backward by n steps.
    """

    def __init__(self, size: int) -> None:
        """
        Parameters
        ----------
        size : int
            The maximum number of states to store.
        """
        self.buffer = deque(maxlen=size)
        self.current_index = -1  # Initialize to -1 to indicate no states yet

    def append(self, state: "State") -> None:
        """
        Appends a state to the buffer.
        """
        if len(self.buffer) == self.buffer.maxlen:
            self.current_index = (self.current_index + 1) % self.buffer.maxlen
        else:
            self.current_index += 1
        self.buffer.append(state)

    def get_last_n_states(self, n: int) -> list["State"]:
        """
        Returns the last n states from the buffer.
        """
        return list(self.buffer)[-n:]

    def get_state_at_index(self, index: int) -> "State":
        """
        Returns the state at the given index.
        """
        if index < 0 or index >= len(self.buffer):
            raise IndexError("Index out of range")
        return self.buffer[index]

    def move_forward(self) -> "State":
        """
        Moves the current index forward by 1 step.
        """
        if self.current_index < len(self.buffer) - 1:
            self.current_index += 1
        else:
            raise IndexError("Already at the most recent state")
        return self.buffer[self.current_index]

    def move_backward(self) -> "State":
        """
        Moves the current index backward by 1 step.
        """
        if self.current_index > 0:
            self.current_index -= 1
        else:
            raise IndexError("Already at the oldest state")
        return self.buffer[self.current_index]

    def __len__(self) -> int:
        """
        Returns the number of states in the buffer.
        """
        return len(self.buffer)

    def __getitem__(self, index: int | slice) -> "State":
        """
        Returns the state at the given index.
        """
        # If index is an integer, return the state at the given index
        if isinstance(index, int):
            # If index is negative, convert it to positive and start from the end
            if index < 0:
                index += len(self.buffer)
            # Check if the index is within the valid range
            if index < 0 or index >= len(self.buffer):
                raise IndexError("Index out of range")
            # Return the state at the given index
            return self.buffer[-1 - index]
        # If index is a slice, return the states in the given range
        elif isinstance(index, slice):
            # Convert the slice to a list of indices
            start, stop, step = index.indices(len(self.buffer))
            # Return the states at the given indices
            return [self[i] for i in range(start, stop, step)]
        else:
            raise TypeError("Invalid argument type")


class TemporalState:
    """
    A temporal state buffer.

    Methods
    -------
    add(state)
        Appends a state to the buffer.
    traverse_forward(n=1)
        Moves the current index forward by n steps.
    traverse_backward(n=1)
        Moves the current index backward by n steps.
    __len__()
        Returns the number of states in the buffer.
    __getitem__(index)
        Returns the state at the given index.
    __call__()
        Returns the current state.

    #! TODO: Finish the time traversing methods
    """

    def __init__(self, state_buffer_size: int) -> None:
        """
        Parameters
        ----------
        state_buffer_size : int
            The maximum number of states to store.
        """
        self.state_buffer_size = state_buffer_size
        self.state_buffer = StateBuffer(state_buffer_size)
        self.relative_index = 0

    def add(self, state: "State") -> None:
        """
        Appends a state to the buffer.
        """
        self.state_buffer.append(state)

    def traverse_forward(self, n: int = 1) -> "State":
        """
        Moves the current index forward by n steps.
        """
        if self._check_index():
            self.relative_index += n
            return self.state_buffer.move_forward()

    def traverse_backward(self, n: int = 1) -> "State":
        """
        Moves the current index backward by n steps.
        """
        if self._check_index():
            self.relative_index -= n
            return self.state_buffer.move_backward()

    def _check_index(self) -> bool:
        """
        Checks if the current index is within the valid range.
        """
        if self.relative_index < 0 or self.relative_index >= len(self.state_buffer):
            raise IndexError("Index out of range")
        return True

    def __len__(self) -> int:
        """
        Returns the number of states in the buffer.
        """
        return len(self.state_buffer)

    def __getitem__(self, index: int | slice) -> "State":
        """
        Returns the state at the given index.
        """
        # ? Should this be relative to the current index?
        return self.state_buffer[index]

    def __call__(self) -> "State":
        """
        Returns the current state.
        """
        return self.state_buffer[self.relative_index]


# Example usage
time_machine = TemporalState(3)
time_machine.add("State 1")
time_machine.add("State 2")
time_machine.add("State 3")
time_machine.add("State 4")

print(f"Time machine[0]: {time_machine[0]}, should be State 4")
print(f"Time machine[1]: {time_machine[1]}, should be State 3")
print(f"Time machine[2]: {time_machine[2]}, should be State 2")
print(f"Time machine[-1]: {time_machine[-1]}, should be State 2")
print(f"Time machine[-2]: {time_machine[-2]}, should be State 3")


assert time_machine[0] == "State 4"
assert time_machine[1] == "State 3"
assert time_machine[2] == "State 2"
assert time_machine[-1] == "State 2"
assert time_machine[-2] == "State 3"

assert time_machine[:] == ["State 4", "State 3", "State 2"]
assert time_machine[1:] == ["State 3", "State 2"]
assert time_machine[::2] == ["State 4", "State 2"]
assert time_machine[:-2] == ["State 4"]
assert time_machine[-2:] == ["State 3", "State 2"]


# Tests
def test_state():
    state = State({"a": 1, "b": 2})
    assert state["a"] == 1
    assert state["b"] == 2


def test_state_buffer():
    state_buffer = StateBuffer(3)
    state_buffer.append("State 1")
    state_buffer.append("State 2")
    state_buffer.append("State 3")
    assert state_buffer[0] == "State 1"
    assert state_buffer[1] == "State 2"
    assert state_buffer[2] == "State 3"


def test_temporal_state():
    temporal_state = TemporalState(3)
    temporal_state.add("State 1")
    temporal_state.add("State 2")
    temporal_state.add("State 3")
    assert temporal_state[0] == "State 1"
    assert temporal_state[1] == "State 2"
    assert temporal_state[2] == "State 3"


def test_temporal_state_traverse():
    temporal_state = TemporalState(3)
    temporal_state.add("State 1")
    temporal_state.add("State 2")
    temporal_state.add("State 3")
    temporal_state.traverse_forward()
    assert temporal_state() == "State 2"


def test_temporal_state_tensor():
    temporal_state = TemporalState(3)
    temporal_state.add("State 1")
    temporal_state.add("State 2")
    temporal_state.add("State 3")
    assert temporal_state.tensor() == torch.tensor([1.0, 2.0, 3.0], dtype=torch.float32)


test_state()
test_state_buffer()
test_temporal_state()
test_temporal_state_traverse()
test_temporal_state_tensor()
