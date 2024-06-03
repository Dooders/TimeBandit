class Ticker:
    """
    A class to represent the ticker of an object
    """

    def __init__(self, cycle: int, step: int, steps_per_cycle: int = 10) -> None:
        """
        Parameters
        ----------
        cycle (int):
            The cycle of the object
        step (int):
            The step of the object
        steps_per_cycle (int):
            The number of steps per cycle
        """
        self.steps_per_cycle = steps_per_cycle
        self.cycle = cycle
        self.step = step

    @property
    def tok(self) -> None:
        """
        Increments the step of the object
        """
        self.step += 1
        if self.step >= self.steps_per_cycle:
            self.cycle += 1
            self.step = 0

        return self.cycle, self.step
