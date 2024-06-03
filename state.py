class ObjectState:
    """
    A class to represent the state of an object

    Attributes
    ----------
    root_id (str):
        The root id of the object
    temporal_id (str):
        The temporal id of the object
    cycle (int):
        The cycle of the object
    step (int):
        The step of the object
    steps_per_cycle (int):
        The number of steps per cycle

    Methods
    -------
    state():
        Returns the state of the object
    encode():
        Future method to encode the object state when requested
    decode(genetics: str):
        Future method to decode the object state from a lower dimensional
        representation in the form of genetics
    """

    def __init__(
        self,
        root_id: str,
        temporal_id: str,
        cycle: int,
        step: int,
        steps_per_cycle: int,
    ) -> None:
        """
        Parameters
        ----------
        root_id (str):
            The root id of the object
        temporal_id (str):
            The temporal id of the object
        cycle (int):
            The cycle of the object
        step (int):
            The step of the object
        steps_per_cycle (int):
            The number of steps per cycle
        """
        self.root_id = root_id
        self.temporal_id = temporal_id
        self.cycle = cycle
        self.step = step
        self.steps_per_cycle = steps_per_cycle

    def state(self) -> dict:
        """
        Returns the state of the object

        Returns
        -------
        dict:
            The state of the object
        """
        return {
            "root_id": self.root_id,
            "temporal_id": self.temporal_id,
            "cycle": self.cycle,
            "step": self.step,
            "steps_per_cycle": self.steps_per_cycle,
        }

    def encode(self) -> str:
        """
        Future method to encode the object state when requested

        Returns
        -------
        genetics (str):
            A lower dimensional representation of the object state
        """
        pass

    def decode(self, genetics: str) -> "ObjectState":
        """
        Future method to decode the object state from a lower dimensional
        representation in the form of genetics

        Parameters
        ----------
        genetics (str):
            A lower dimensional representation of the object state

        Returns
        -------
        ObjectState:
            A new object state object with the decoded state
        """
        pass


class Object:
    """
    A class to represent an object

    Attributes
    ----------
    steps_per_cycle (int):
        The number of steps per cycle
    root_id (str):
        The root id of the object
    temporal_id (str):
        The temporal id of the object

    Methods
    -------
    update():
        Updates the object state
    encode_self():
        Encodes the object state
    id(encode: bool = True):
        Returns the id of the object
    state():
        Returns the state of the object
    """

    steps_per_cycle: int
    root_id: str
    temporal_id: str

    def __init__(self, steps_per_cycle: int = 1) -> None:
        """
        Parameters
        ----------
        steps_per_cycle (int):
            The number of steps per cycle
        """
        self.steps_per_cycle = steps_per_cycle
        self._cycle = 1
        self._step = 0
        self.root_id = "root"  #! Will automatically be updated
        self.temporal_id = "temporal"

    def __str__(self) -> str:
        return self.id(encode=False)

    def __repr__(self) -> str:
        return self.id(encode=False)

    def update(self) -> dict:
        """
        Updates the object state

        Returns
        -------
        dict:
            The state of the object
        """
        self._step += 1
        if self._step == self.steps_per_cycle:
            self._cycle += 1
            self._step = 0

        return self.state

    def encode_self(self) -> None:
        """
        Encodes the object state
        """
        self.temporal_id = f"{self.root_id}.{self._cycle}.{self._step}"

    def id(self, encode: bool = True) -> str:
        """
        Returns the id of the object

        Parameters
        ----------
        encode (bool):
            Whether to encode the object state or not

        Returns
        -------
        str:
            The id of the object
        """
        if encode:
            self.encode_self()

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
        return ObjectState(
            self.root_id,
            self.temporal_id,
            self._cycle,
            self._step,
            self.steps_per_cycle,
        ).state()

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
