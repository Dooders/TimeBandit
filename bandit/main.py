from bandit.space import Space
from bandit.time import Time




class TimeBandit:
    def __init__(self):
        self.time_graph = Time()
        self.space_graph = Space()

    def tick(self):
        self._time += 1

    def get_time(self):
        return self._time
