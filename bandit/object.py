import uuid


class Object:
    """
    A class to represent an object

    Attributes
    ----------
    steps_size (int):
        The number of steps per cycle
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
        self._cycle = 1
        self._step = 0
        self.root_id = uuid.uuid4().hex
        self.temporal_id = self.encode()

    def __str__(self) -> str:
        return self.id()

    def __repr__(self) -> str:
        return self.id()

    def update(self) -> dict:
        """
        Updates the object state

        Returns
        -------
        dict:
            The state of the object
        """

        if self._step < self.steps_size - 1:
            self._step += 1
        else:
            self._step = 0
            self._cycle += 1

        self.temporal_id = self.encode()

        return self.state

    def encode(self) -> str:
        """
        Encodes the object state
        """
        return f"{self.root_id}.{self._cycle}.{self._step}"

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
            "cycle": self._cycle,
            "step": self._step,
            "root_id": self.root_id,
            "temporal_id": self.temporal_id,
        }

    @property
    def cycle(self) -> int:
        """
        Returns the cycle of the object
        """
        return self._cycle

    @property
    def step(self) -> int:
        """
        Returns the step of the object
        """
        return self._step
