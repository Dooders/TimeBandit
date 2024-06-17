import time


class Clock:
    """
    A clock that can be used to step through a series of steps.

    Methods
    --------
    update()
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

    def __init__(self, steps_per_cycle: int, starting_time: str = "1.0") -> None:
        """
        Initializes the clock.

        Parameters
        ----------
        steps_per_cycle
            The number of steps per cycle.
        starting_time
            The starting time in the format of "{cycle}:{step}".
        """
        self.steps_per_cycle = steps_per_cycle
        self.starting_time = starting_time
        self._cycle = 1
        self._step = 0
        self._start_time = time.time()

    def update(self) -> None:
        """
        Steps the clock by 1 step.
        Updates the object's step and cycle properties.
        """
        self._step += 1
        if self._step >= self.steps_per_cycle:
            self._cycle += 1
            self._step = 0

        return self._cycle, self._step

    def clone(self) -> "Clock":
        """
        Returns a clone of the clock with the same steps_per_cycle and current time in the simulation

        Returns
        --------
        Clock
            A clone of the clock with the same steps_per_cycle and current time in the simulation
        """
        return Clock(self.steps_per_cycle, self.starting_time)

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

    @property
    def cycle(self) -> int:
        """
        Returns the current cycle number.
        """
        return self._cycle

    @property
    def step(self) -> int:
        """
        Returns the current step number.
        """
        return self._step
