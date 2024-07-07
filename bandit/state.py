"""
A state management system for TimeBandit.

Using objects to encapsulate state and behavior, each entity in the simulation 
is represented by an object. This approach facilitates easy state management 
and manipulation.

The TemporalState class stores an object's state in a temporal sense, utilizing a 
StateBuffer. The StateBuffer is a deque with a specified maxlen, where the 
current_index indicates the position of the current state within the buffer.

This system allows for:
- State saving and restoration: Capture the current state and restore to a previous 
  state as needed.
- State compression and decompression: Efficiently manage memory and storage 
  through compression techniques.
- State storage and retrieval: Access and persist state data for future use.
- State traversal through the temporal state buffer: Navigate through historical 
  states within the buffer.
- Objects with varying state buffer sizes and functionality: Customize the buffer 
  size and capabilities for different objects, enabling flexible and adaptive state 
  management.

By encapsulating state and behavior within objects and managing these states temporally, 
the system provides a robust framework for simulating dynamic and complex entities in 
TimeBandit.

NOTES
-----
- I've gone with an object oriented state management system. Using objects to 
    encapsulate state and behavior. Each entity in the simulation is represented 
    by an object. This allows for easy state management and manipulation.
    It also allows for easy state restoration. It also allows for easy state 
    compression and decompression. It also allows for easy state storage and 
    retrieval.


TODO
----
- More intuitive API to get state and state values
- Implement the encode and decode methods in the ObjectState class. Would need
    to encode the object state into a single string, and then decode it back to 
    original state. This will give the ability to store the state of an object 
    in a database and easily reinstate it
- Experiment with an auto-encoder to compress the object state into a lower 
    dimensional representation that can recombine with genetic algorithms. 
    Then use the decoder to decompress the state back into the original state. 
    The idea is to get the minimal amount of information needed to reinstate the 
    object state within a range of error, which serves as a mutation mechanism if 
    using evolutionary algorithms.
- Maybe an evolutionary approach to an auto-encoder that slowly compresses the 
    encoding more and more, as long as the decoding output is correct. Will 
    hopefully need less and less context/information to reinstate the object 
    from the encoded data. Starts with the least compressions, so how far it 
    can get and be accurate, then increase the compression and do the same, until 
    it no longer worth it to keep going
- Hybrid state management system blending object-oriented with ECS.
"""

from collections import deque
from typing import TYPE_CHECKING

import torch

if TYPE_CHECKING:
    from bandit.object import Object


class State(dict):
    """
    A state in the temporal state buffer.
    Extends dict to allow for arbitrary state data.

    Methods
    -------
    encode()
        Encodes the state to another state.
    decode()
        Decodes the state to another state.
    tensor()
        Returns the state as a tensor.

    TODO
    ----
    - Provide a mapping as part of the _flatten method to reconstruct the state
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

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
        return [value for value in self.values()]

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

    TODO
    ----
    - Implement slicing
    - Make sure indexing works as expected
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
        return self[index]

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
            # If index is negative
            if index < 0:
                index = abs(index)
            # Check if the index is within the valid range
            if index < 0 or index >= len(self.buffer):
                raise IndexError("Index out of range")
            # Return the state at the given index
            return self.buffer[-1 - index]
        # If index is a slice, return the states in the given range
        elif isinstance(index, slice):
            raise NotImplementedError("Haven't implemented slicing yet")
            #! Highlighted out until implemented
            # # Convert the slice to a list of indices
            # start, stop, step = index.indices(len(self.buffer))
            # # Return the states at the given indices
            # return [self[i] for i in range(start, stop, step)]
        else:
            raise TypeError("Invalid argument type")


class TemporalState:
    """
    A temporal state buffer.

    Attributes
    ----------
    state_buffer_size : int
        The maximum number of states to store.
    state_buffer : StateBuffer
        The state buffer.
    relative_index : int
        The relative index of the current state.

    Methods
    -------
    add(state)
        Appends a state to the buffer.
    traverse_forward(n=1)
        Moves the current index forward by n steps.
    traverse_backward(n=1)
        Moves the current index backward by n steps.

    TODO
    ----
    - Finish the time traversing process
    """

    def __init__(self, state_buffer_size: int = 1000) -> None:
        """
        Parameters
        ----------
        state_buffer_size : int
            The maximum number of states to store.
        """
        self.state_buffer_size = state_buffer_size
        self.state_buffer = StateBuffer(state_buffer_size)
        self.relative_index = 0

    def _add(self, state: "State") -> None:
        """
        Appends a state to the buffer.
        """
        self.state_buffer.append(state)

    def update(self, object: "Object") -> "State":
        """
        Updates the State.
        """
        object_state = State(
            cycle=object.clock.cycle,
            step=object.clock.step,
            root_id=object.id.root,
            temporal_id=object.id.temporal,
        )
        self._add(object_state)

        return object_state

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

        Returns
        -------
        bool
            Whether the index is within the valid range.
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
        return self.state_buffer[index]

    def __call__(self) -> "State":
        """
        Returns the current state.
        """
        if len(self.state_buffer) == 0:
            raise IndexError("No states in the buffer")
        return self.state_buffer[self.relative_index]
