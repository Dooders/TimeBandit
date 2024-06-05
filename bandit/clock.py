import time

from bandit.object import Object


class Clock:
    """
    A clock that can be used to step through a series of steps.

    Methods
    --------
    step(object)
        Steps the clock by 1 step.
        Updates the object's step and cycle properties.

    Properties
    -----------
    cycle
        The current cycle number.
    step
        The current step number.
    time
        The current time in the format of "{cycle}:{step}".
    real_time
        The real time since the clock was started.
    """

    def __init__(self, steps_per_cycle: int) -> None:
        self.steps_per_cycle = steps_per_cycle
        self._cycle = 1
        self._step = 0
        self._start_time = time.time()

    def step(self, object: "Object") -> None:
        """
        Steps the clock by 1 step.
        Updates the object's step and cycle properties.

        Parameters
        ----------
        object
            The object to update.
        """
        self._step += 1
        if self._step >= self.steps_per_cycle:
            self._cycle += 1
            self._step = 0

        # update the object's step and cycle properties
        object.step = self._step
        object.cycle = self._cycle

    @property
    def cycle(self) -> int:
        return self._cycle

    @property
    def step(self) -> int:
        return self._step

    @property
    def time(self) -> float:
        """
        Returns the current time in the format of "{cycle}:{step}".
        """
        return f"{self._cycle}:{self._step}"

    @property
    def real_time(self) -> float:
        """
        Returns the real time since the clock was started.
        """
        return time.time() - self._start_time
