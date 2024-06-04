from bandit.object import Object
from bandit.space import Space
from bandit.ticker import Ticker
from bandit.time import Time


class TimeBandit:
    def __init__(self):
        self.time = Time()
        self.space = Space()
