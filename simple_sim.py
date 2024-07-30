from fizicks import Motion, Position, Velocity

from bandit.object import Object
from bandit.space import Space

space = Space()

class Ball(Object):
    def __init__(self, position, velocity, mass):
        super().__init__()
        self.position = Position(*position)
        self.velocity = Velocity(*velocity)
        self.mass = mass
        self.debt = []

    def _update(self):
        Motion.update(self)

    def state(self):
        state = super().state()

        return {
            "position": self.position,
            "velocity": self.velocity,
            "mass": self.mass,
            "debt": self.debt,
            **state,
        }


ball = Ball([0, 0, 0], [1, 0, 0], 1)
space.add_object(ball)
print(space.state())
print('***********************')
space.update()
print(space.state())
