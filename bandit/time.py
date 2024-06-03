from bandit.graph import Graph
from bandit.state import Object


class Time(Graph):
    """
    Time class is a directed graph that represents the time of objects.
    It is a subclass of networkx.DiGraph.

    Methods
    -------
    add_thread(object1, object2):
        Adds a thread between two objects
    remove_thread(object1, object2):
        Removes a thread between two objects
    """

    def __init__(self):
        super().__init__()
        self.time = int(f"{self._cycle}.{self._step}")

    def add_thread(self, object1: "Object", object2: "Object") -> None:
        """
        Adds a thread between two objects

        Parameters
        ----------
        object1 (Object):
            The first object
        object2 (Object):
            The second object
        """
        self.add_edge(object1, object2)

    def remove_thread(self, object1: "Object", object2: "Object") -> None:
        """
        Removes a thread between two objects

        Parameters
        ----------
        object1 (Object):
            The first object
        object2 (Object):
            The second object
        """
        self.remove_edge(object1, object2)
