from bandit.graph import Graph


class Time(Graph):
    """
    Time class is a directed graph that represents the time of objects.
    It is a subclass of networkx.DiGraph.

    Attributes
    ----------
    time (str):
        The time of the time
    temporal_id_cache (dict):
        A dictionary that maps temporal ids to objects

    Methods
    -------
    add_thread(object1, object2):
        Adds a thread between two objects
    remove_thread(object1, object2):
        Removes a thread between two objects
    """

    def __init__(self):
        super().__init__()
        self.time = f"Time: {self.cycle} {self.step}"
        self.temporal_id_cache = {}

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
            print(f"Adding object {object} to time")
            temporal_id = object.get("temporal_id", 0)
            root_id = object.get("root_id", None)
            self.add_node(temporal_id, **object)
            new_temporal_cache[temporal_id] = root_id
