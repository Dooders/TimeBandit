"""
Identity module for handling object identities in the simulation.

Including creation and handling of the root and temporal IDs
"""

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bandit.clock import Clock


class Identity:
    """
    Identity class for handling object identities in the simulation.

    Attributes
    ----------
    root : str
        The root ID of the object.
    temporal : str
        The temporal ID of the object. Unique for every step of the simulation.

    Methods
    -------
    update(clock: Clock) -> None
        Updates the temporal ID of the object based on the current clock.
    """

    def __init__(self) -> None:
        self.root: str = uuid.uuid4().hex
        self.temporal: str = f"{self.root}.1.0"

    def __call__(self, root: bool = False) -> str:
        """
        Returns the root or temporal ID of the object.

        Parameters
        ----------
        root : bool, default False
            If True, returns the root ID. Otherwise, returns the temporal ID.

        Returns
        --------
        str
            The root or temporal ID of the object.
        """
        if root:
            return self.root
        else:
            return self.temporal

    def update(self, clock: "Clock") -> None:
        """
        Updates the temporal ID of the object based on the current clock.
        """
        self.temporal = f"{self.root}.{clock.cycle}.{clock.step}"
