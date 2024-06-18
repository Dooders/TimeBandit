"""
An object is a fundamental component of TimeBandit represented as a specialized node in the 
simulation that is updated and has a state

The Object class is designed to contain the state of the object and its update method

An object exists in a Space and is anchored to a Point in Time.

An object can be tied to other agents in the same space and can be used to model
a variety of phenomena such as the weather, the growth of a population, the 
traffic flow in a city, or the spread of a disease.

Example
-------
Consider a weather object that exists in a space and is anchored to a point in time.
The weather object can be used to model the weather in a city and can be tied to other
objects in the same space to model the weather in a city.

Here is how you can create an object in code

```python
weather = Object()
```

"""

import uuid

from bandit.clock import Clock


class Object:
    """
    A class to represent an object in a simulation

    Attributes
    ----------
    steps_size (int):
        The number of steps per cycle
    clock (Clock):
        The clock of the object
    root_id (str):
        The root id of the object
    temporal_id (str):
        The temporal id of the object

    Methods
    -------
    update():
        Updates the object state
    encode():
        Encodes the object state
    id(root: bool = False):
        Returns the id of the object, temporal_id by default
    state():
        Returns the state of the object
    cycle():
        Returns the cycle of the object
    step():
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

    def __str__(self) -> str:
        return f"{self.__class__.__name__}:{self.root_id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}:{self.root_id}"

    def update(self) -> dict:
        """
        Updates the object state

        Returns
        -------
        dict:
            The state of the object
        """

        self.clock.update()
        self.temporal_id = self.encode()

        return self.state

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

    @property
    def state(self) -> dict:
        """
        Returns the state of the object

        Returns
        -------
        dict:
            The state of the object
        """
        return {
            "cycle": self.clock.cycle,
            "step": self.clock.step,
            "root_id": self.root_id,
            "temporal_id": self.temporal_id,
        }

    @property
    def cycle(self) -> int:
        """
        Returns the cycle of the object
        """
        return self.clock.cycle

    @property
    def step(self) -> int:
        """
        Returns the step of the object
        """
        return self.clock.step
