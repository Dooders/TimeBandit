"""
An object is a fundamental component of TimeBandit represented as a specialized 
node in the simulation that is updated and has a state

The Object class is designed to contain the state of the object and its update 
method, and exists in a Space and is anchored to a Point in Time.

An object can be tied to other agents in the same space and can be used to model
a variety of phenomena such as the weather, the growth of a population, the 
traffic flow in a city, or the spread of a disease, etc.
"""

import pickle
import uuid

from bandit.clock import Clock
from bandit.state import State, TemporalState


class Object:
    """
    A class to represent an object in a simulation

    Attributes
    ----------
    steps_size (int):
        The number of steps per cycle. For example, if steps_size is 5, a cycle
        is counted every 5 steps.
    clock (Clock):
        The clock of the object, contains the relative time of the object in
        cycles and steps
    root_id (str):
        The root id of the object
    temporal_id (str):
        The temporal id of the object, contains the root_id and the clock for a
        specific object instance
    state (TemporalState):
        Includes buffered previous states

    Methods
    -------
    update():
        Updates the object state
    encode():
        Encodes the object state
    id(root: bool = False):
        Returns the id of the object, temporal_id by default

    save(path: str):
        Pickle object to file, saved to path/root_id
    load(path: str):
        Load object from file

    Properties
    ----------
    record_state:
        Returns the current state of the object
    cycle:
        Returns the cycle of the object
    step:
        Returns the step of the object
    """

    def __init__(self, steps_size: int = 1) -> None:
        """
        Parameters
        ----------
        steps_per_cycle (int):
            The number of steps per cycle
        """
        self.steps_size = steps_size
        self.clock = Clock(steps_size)
        self.root_id = uuid.uuid4().hex
        self.temporal_id = self.encode()
        self.state = TemporalState(100000)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}:{self.root_id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}:{self.root_id}"

    def update(self) -> dict:
        """
        Updates the object state and returns the state after the update.

        Updates the clock and the temporal_id.

        Returns
        -------
        dict:
            The state of the object
        """

        self.clock.update()
        self.temporal_id = self.encode()

        return self.record_state

    def encode(self) -> str:
        """
        Encodes the object state
        """
        return f"{self.root_id}.{self.clock.cycle}.{self.clock.step}"

    def id(self, root: bool = False) -> str:
        """
        Returns the id of the object

        Parameters
        ----------
        root (bool):
            Whether to return the root id or the temporal id

        Returns
        -------
        str:
            The id of the object
        """
        if root:
            return self.root_id

        return self.temporal_id

    def save(self, path: str) -> str:
        """
        Pickle object to file, saved to path/root_id
        """
        full_path = f"{path}/{self.root_id}"
        with open(full_path, "wb") as f:
            pickle.dump(self, f)
        return full_path

    @classmethod
    def load(cls, path: str) -> "Object":
        """
        Load object from file
        """
        with open(path, "rb") as f:
            obj = pickle.load(f)
        return obj

    @property
    def record_state(self) -> State:
        """
        Returns the state of the object.

        Automatically adding it to the state_buffer in the process.

        Returns
        -------
        State:
            A dict-like object containing the current state of the object
        """
        object_state = State(
            cycle=self.clock.cycle,
            step=self.clock.step,
            root_id=self.root_id,
            temporal_id=self.temporal_id,
        )
        self.state.add(object_state)

        return object_state

    @property
    def cycle(self) -> int:
        """
        Returns the relative cycle of the object
        """
        return self.clock.cycle

    @property
    def step(self) -> int:
        """
        Returns the relative step of the object
        """
        return self.clock.step
