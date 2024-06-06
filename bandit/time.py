from bandit.graph import Graph
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bandit.object import Object

class Time(Graph):
    """
    Time class is a directed graph that represents the time of objects.
    It is a subclass of networkx.DiGraph.

    Attributes
    ----------
    time (str):
        The time of the time
    root_id_cache (dict):
        A dictionary that maps temporal ids to objects

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
        self.root_id_cache = {}

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
        Adds a space to the time

        Parameters
        ----------
        space_state (dict):
            The state of the space
        """
        new_temporal_cache = {}
        
        for object in space_state.values():
            temporal_id = object.get("temporal_id", 0)
            root_id = object.get("root_id", None)
            self.add_node(temporal_id, **object)
            new_temporal_cache[temporal_id] = root_id

        # Add threads to any matching root_ids in the root_id_cache
        for temporal_id, root_id in self.root_id_cache.items():
            if root_id in space_state:
                self.add_thread(temporal_id, space_state[root_id])

        self.root_id_cache = new_temporal_cache


    def threads(self) -> list:
        """
        Returns the threads in the time
        """
        return self.edges(data=True)
