from temporal import TemporalObject

from bandit.clock import Clock
from bandit.space import Space


class TimeBandit:
    """
    The main class for the TimeBandit simulation.

    Parameters
    ----------
    space (Space):
        The space to simulate.
    temporal_depth (int):
        The depth of the temporal object.

    Methods
    -------
    update():
        Update the simulation.
    run(steps: int):
        Run the simulation for a given number of steps.
    state():
        Return the state of the simulation.
    """

    def __init__(self, space: Space, temporal_depth: int = 100):
        self.time = TemporalObject(temporal_depth)
        self.clock = Clock()
        self.space = space

    def update(self) -> None:
        """
        Update the simulation.
        """
        self.clock.update()
        self.space.update()
        self.time.update(self.space.state(), self.clock.time)

    def run(self, steps: int) -> None:
        """
        Run the simulation for a given number of steps.
        """
        for _ in range(steps):
            self.update()

    def state(self) -> dict:
        """
        Return the state of the simulation.
        """
        return self.time.current
