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

from bandit.util import LimitedDict

if TYPE_CHECKING:
    from bandit.object import Object
    from bandit.state import State


class TemporalBuffer:
    """
    A buffer designed for storing and managing states in a temporal sequence.

    This class utilizes a deque with a fixed maximum length (maxlen) to maintain
    a rolling buffer of states.

    Each state can be indexed by an integer, a string ID, or a slice. The class
    also tracks the current state index within the buffer.

    Parameters
    ----------
    temporal_depth : int
        The maximum number of states to store.

    Attributes
    ----------
    buffer : deque
        A deque with a maxlen.
    id_index : LimitedDict
        A dictionary with a limit on the number of items it can store.
    current_index : int
        The index of the current state.

    Methods
    -------
    add(id: str, state: State) -> None:
        Appends a state to the buffer.
    update(object) -> None:
        Adds the object's state to the buffer.
    get_last_n_states(n: int) -> list[State]:
        Returns the last n states from the buffer.
    get_state_at_index(index: int) -> State:
        Returns the state at the given index.
    move_forward() -> State:
        Moves the current index forward by 1 step.
    move_backward() -> State:
        Moves the current index backward by 1 step.
    current() -> State:
        Returns the current state.
    """

    def __init__(self, temporal_depth: int = 100) -> None:
        """
        Parameters
        ----------
        size : int
            The maximum number of states to store.
        """
        self.buffer = deque(maxlen=temporal_depth)
        self.id_index = LimitedDict(temporal_depth)
        self.current_index = -1  # Initialize to -1 to indicate no states yet

    def add(self, id: str, state: "State") -> None:
        """
        Appends a state to the buffer.

        Parameters
        ----------
        id : str
            The ID of the state.
        state : State
            The state to add to the buffer.
        """
        self.id_index[id] = state
        if len(self.buffer) == self.buffer.maxlen:
            self.current_index = (self.current_index + 1) % self.buffer.maxlen
        else:
            self.current_index += 1
        self.buffer.append(state)

    def update(self, object: "Object") -> None:
        """
        Adds the object's state to the buffer.

        Parameters
        ----------
        object : Object
            The object to add to the buffer.
        """
        self.add(object.id.temporal, object.state)

    def get_last_n_states(self, n: int) -> list["State"]:
        """
        Returns the last n states from the buffer.

        Parameters
        ----------
        n : int
            The number of states to return.

        Returns
        -------
        list[State]
            The last n states from the buffer.
        """
        return list(self.buffer)[-n:]

    def get_state_at_index(self, index: int) -> "State":
        """
        Returns the state at the given index.

        Parameters
        ----------
        index : int
            The index of the state to return.

        Returns
        -------
        State
            The state at the given index.
        """
        return self[index]

    def move_forward(self) -> "State":
        """
        Moves the current index forward by 1 step.

        Returns
        -------
        State
            The state at the new index.
        """
        raise NotImplementedError("Forward traversal not implemented")

    def move_backward(self) -> "State":
        """
        Moves the current index backward by 1 step.

        Returns
        -------
        State
            The state at the new index.
        """
        raise NotImplementedError("Backward traversal not implemented")

    def _get_by_temporal_id(self, temporal_id):
        return self.id_index.get(temporal_id, None)

    def __len__(self) -> int:
        """
        Returns the number of states in the buffer.

        Returns
        -------
        int
            The number of states in the buffer.
        """
        return len(self.buffer)

    def __call__(self, index: int | slice | str = 0) -> "State":
        """
        Returns the state at the given index.
        """
        if len(self.buffer) == 0:
            raise IndexError("No states in the buffer")
        return self.buffer[index]

    def __contains__(self, key: str) -> bool:
        """
        Returns whether the temporal ID is in the buffer.
        """
        return key in self.id_index

    def __setitem__(self, key: str, value: "State") -> None:
        """
        Sets the value of the key.
        """
        self.id_index[key] = value

    def __delitem__(self, key: str) -> None:
        """
        Deletes the value of the key.
        """
        del self.id_index[key]

    def __iter__(self) -> "State":
        """
        Returns an iterator over the states in the buffer.
        """
        return iter(self.buffer)

    def __getitem__(self, index: int | slice | str) -> "State":
        """
        Returns the state at the given index.

        Parameters
        ----------
        index : int | slice | str
            The index of the state to return. Can be by position (int),
            by temporal ID (str), or by slice.

        Returns
        -------
        State
            The state at the given index.
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

        elif isinstance(index, str):
            return self._get_by_temporal_id(index)
        else:
            raise TypeError("Invalid argument type")

    @property
    def current(self) -> "State":
        """
        Returns the current state.

        Returns
        -------
        State
            The current state.
        """
        return self.buffer[-1]
