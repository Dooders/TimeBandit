from collections import deque
from typing import Any


class State(dict):
    """
    A state in the temporal state buffer.
    Extends dict to allow for arbitrary state data.
    """

    def __init__(self, state: Any) -> None:
        self.state = state


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
