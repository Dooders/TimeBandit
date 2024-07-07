import time

from bandit.data import ClockState, Cycle, Step


class Clock:
    """
    A clock that can be used to step through a series of steps.

    Methods
    --------
    update()
        Steps the clock by 1 step.
        Updates the object's step and cycle properties.
    reset()
        Resets the clock to the starting time.
    clone()
        Returns a clone of the clock with the same steps_per_cycle and current
        time in the simulation

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

    TODO
    ----
    - Improve clone() logic
    """

    def __init__(self, steps_per_cycle: int = 10) -> None:
        """
        Initializes the clock.

        Parameters
        ----------
        steps_per_cycle
            The number of steps per cycle. For example, 10 steps per cycle would
            be 1:0, 1:1, 1:2, ..., 1:9, 2:0, 2:1, ...
        """
        self.steps_per_cycle = steps_per_cycle
        self._cycle: Cycle = 1
        self._step: Step = 0
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

    def clone(self) -> "Clock":
        """
        Returns a clone of the clock with the same steps_per_cycle and current time in the simulation

        Returns
        --------
        Clock
            A clone of the clock with the same steps_per_cycle and current time in the simulation
        """
        clock = Clock(self.steps_per_cycle)
        clock._cycle = self._cycle
        clock._step = self._step
        clock._start_time = self._start_time
        return clock

    def reset(self) -> None:
        """
        Resets the clock to the starting time.
        """
        self._cycle: Cycle = 1
        self._step: Step = 0

    def __str__(self) -> str:
        """
        Returns the current time in the format of "{cycle}:{step}".
        """
        return f"{self._cycle}:{self._step}"

    def __repr__(self) -> str:
        """
        Returns the current time in the format of "{cycle}:{step}".
        """
        return f"{self._cycle}:{self._step}"

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
    def cycle(self) -> "Cycle":
        """
        Returns the current cycle number.
        """
        return self._cycle

    @property
    def step(self) -> "Step":
        """
        Returns the current step number.
        """
        return self._step

    @property
    def state(self) -> "ClockState":
        """
        Returns the current state of the clock.
        """
        return ClockState(cycle=self._cycle, step=self._step)
