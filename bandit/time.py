"""
The Time module is designed to represent the temporal state of objects in a
?concrete? space. It is a directed graph that stores connections between object
states in specialized edges called Threads. Where a thread connects an 
object state to its previous object state, back to the initial object state.
"""

from typing import TYPE_CHECKING

from bandit.graph import Graph

if TYPE_CHECKING:
    from bandit.object import Object


#! TODO: Create data class for space_state, temporal_id, root_id, and object_id
#! TODO: Find better way to communicate object state of interest and reference previous (or even future) states (time subscript_i ??)
#! TODO: ThreadView class to represent threads (working like EdgeView???)
#! TODO: TimeView class to represent the time (working like NodeView???)


class Time(Graph):
    """
    Time class is a directed graph that represents the time of objects.
    It is a subclass of networkx.DiGraph.

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
