from bandit.ticker import Ticker
from bandit.util import generate_hash


def temporal_id(root_id: str, cycle: int, step: int) -> str:
    """
    Returns the temporal id of an object

    Parameters
    ----------
    root_id (str):
        The root id of the object
    cycle (int):
        The cycle of the object
    step (int):
        The step of the object

    Returns
    -------
    str:
        The temporal id of the object
    """
    return f"{root_id}.{cycle}.{step}"


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
    encode_self():
        Encodes the object state
    id(encode: bool = True):
        Returns the id of the object
    state():
        Returns the state of the object
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
        self.root_id = "root_id"
        self.temporal_id = "temporal_id"
        self.root_id = generate_hash(self.state)
        self.temporal_id = temporal_id(self.root_id, self._cycle, self._step)

        self.tic = Ticker(
            self._cycle, self._step, self.steps_size
        )  #! Make a global ticker class that handles the primary clock and allows independent sub clocks

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

        self._cycle, self._step = self.tic.tok
        self.root_id = generate_hash(self)

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
