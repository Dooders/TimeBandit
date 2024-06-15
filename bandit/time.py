"""
The Time module is designed to contain the temporal state of objects within a 
dynamically structured space. This space is specific and organized, not a wide-open, 
undefined environment, allowing for precise and adaptive temporal modeling.

It functions as a directed graph, storing connections between object states in 
specialized edges called Threads. Each thread links an object state at a given time 
step (t_i) to its state at the previous time step (t_{i-1}), tracing back to the 
initial object state (t_0). This notation, referred to here as Temporal Notation, can 
also extend to future states (t_{i+1}), thereby creating a coherent temporal sequence.

Temporal Notation
-----------------
Temporal Notation is a system used to reference the state of objects at specific 
points in time, both objectively within the simulation and relatively for specific 
objects. 

Objective Temporal Notation
---------------------------
Objective Temporal Notation refers to the overall timeline of the simulation. Each 
state is denoted by a subscript indicating its position in the global sequence of 
time steps.

- t_i: The current state at the global time step i.
- t_{i-1}: The previous state at the global time step i-1.
- t_0: The initial state at the starting time step.
- t_{i+1}: The future state at the global time step i+1.

Relative Temporal Notation
---------------------------
Relative Temporal Notation refers to the timeline of an individual object within the 
simulation. Each state is denoted by a subscript indicating its position in the 
object's own sequence of time steps.

- t_0^obj: The current state of the object.
- t_-1^obj: The previous state of the object at its local time step i-1.
- t_+1^obj: The future state of the object at its local time step i+1.

Use
---
Temporal Notation helps in clearly identifying and referencing the states of objects 
as they evolve over time, both from a global simulation perspective and an individual 
object perspective. It provides a consistent and concise way to trace the sequence of 
states and the transitions between them.

Example
-------
Consider an object that changes its state over three global time steps. The states 
can be denoted as follows:

Objective Temporal Notation:
- t_0: Initial global state
- t_1: Global state at time step 1
- t_2: Global state at time step 2

Relative Temporal Notation for an object:
- t_0^obj: Current state of the object
- t_-1^obj: State of the object from the previous step
- t_-2^obj: State of the object from the -2 steps

In the Time module, a Thread connects these states to form a directed sequence:
t_0 -> t_1 -> t_2 (Objective)
t_-2^obj <- t_-1^obj <- t_0^obj (Relative)

Here is how you might add these states and threads in code:

    from time_module import Time, Object

    time_graph = Time()

    initial_state = Object(temporal_id=0, data=...)
    state1 = Object(temporal_id=1, data=...)
    state2 = Object(temporal_id=2, data=...)

    time_graph.add_space({initial_state.temporal_id: initial_state})
    time_graph.add_space({state1.temporal_id: state1})
    time_graph.add_space({state2.temporal_id: state2})

    print(time_graph.threads())
"""

from typing import TYPE_CHECKING

from bandit.graph import Graph

if TYPE_CHECKING:
    from bandit.object import Object


#! TODO: Create data class for space_state, temporal_id, root_id, object_id, and root_id_cache
#! TODO: ThreadView class to represent threads (working like EdgeView???)
#! TODO: TimeView class to represent the time (working like NodeView???)
#! TODO: Design out ObjectiveTime and RelativeTime
#! TODO: Better way to represent time other than incrementing integers
#! TODO: Exception handling and unit testing
#! TODO: Add threads to spaces???? Is that even needed?


class Time(Graph):
    """
    Time class is a directed graph that represents the time of objects.
    It is a subclass of the Graph class.

    A Thread is a directed edge between an object state in the previous
    time and the object state in the current time.

    Methods
    -------
    add_thread(object_a, object_b):
        Adds a thread between two objects
    remove_thread(object_a, object_b):
        Removes a thread between two objects
    threads():
        Returns the threads in the time
    """

    def __init__(self):
        super().__init__()
        self._root_id_cache = {}

    def add_thread(self, object_a: "Object", object_b: "Object") -> None:
        """
        Adds a thread between two objects

        Parameters
        ----------
        object_a (Object):
            The first object
        object_b (Object):
            The second object
        """
        self.add_edge(object_a, object_b, type="thread")

    def remove_thread(self, object_a: "Object", object_b: "Object") -> None:
        """
        Removes a thread between two objects

        Parameters
        ----------
        object_a (Object):
            The first object
        object2 (Object):
            The second object
        """
        self.remove_edge(object_a, object_b)

    def add_space(self, space_state: dict) -> None:
        """
        Adds a space to the time as well as adding threads to the previous
        root object.

        Parameters
        ----------
        space_state (dict):
            The state of the space
        """
        new_temporal_cache = {}

        # Add current object states to the time graph
        for object in space_state.values():
            temporal_id = object.get("temporal_id", 0)
            root_id = object.get("root_id", None)
            self.add_node(temporal_id, **object)
            new_temporal_cache[root_id] = temporal_id

        # Add threads to any matching root_ids between the previous
        # and current object states
        for root_id, temporal_id in self._root_id_cache.items():
            if root_id in new_temporal_cache:
                self.add_thread(temporal_id, new_temporal_cache[root_id])

        self._root_id_cache = new_temporal_cache

    def threads(self) -> list:
        """
        Returns the threads in the time
        """
        return self.edges(data=True)


"""
I want to test:
- New object states get added correctly
- Threads get added correctly
- Threads get removed correctly
- Threads get added between new and old object states
- Object states in threads are as expected
"""
