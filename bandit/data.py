"""
Pydantic data models for the TimeBandit
"""

from pydantic import Field

from bandit.state import State

__cycle_description__ = "A period of time that is divided into steps. A cycle can be made up of any number of steps."
__step_description__ = (
    "A step in a cycle. A step is a unit of time that is a fraction of a cycle."
)
__root_description__ = "The root id of the object."
__temporal_description__ = "An id that is unique within a temporal context."

Cycle: int = Field(..., description=__cycle_description__)
Step: int = Field(..., description=__step_description__)
Root: str = Field(..., description=__root_description__)
Temporal: str = Field(..., description=__temporal_description__)
Temporal: str = Field(..., description=__temporal_description__)


class ClockState(State):
    cycle: Cycle
    step: Step


class IdentityState(State):
    root: Root
    temporal: Temporal


class ConnectionsState(State):
    pass


class InteractionsState(State):
    pass


class ObjectState(State):
    clock: ClockState
    id: IdentityState
    connections: ConnectionsState
    interactions: InteractionsState
