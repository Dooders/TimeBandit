import networkx as nx


class Time(nx.DiGraph):
    """
    Time class is a directed graph that represents the time of objects.
    It is a subclass of networkx.DiGraph.

    Methods
    -------
    add_object(object):
        Adds an object to the time
    remove_object(object):
        Removes an object from the time
    add_thread(object1, object2):
        Adds a thread between two objects
    remove_thread(object1, object2):
        Removes a thread between two objects
    get_state(object_id):
        Returns the state of the object
    get_object(object_id):
        Returns the object
    draw_time():
        Draws the time
    update():
        Updates the object state
    """

    def __init__(self):
        super().__init__()
        self._input = None
        self._output = None
        self._step = 0
        self._cycle = 0
        self.time = int(f"{self._cycle}.{self._step}")

    def add_object(self, object) -> None:
        """
        Adds an object to the time

        Parameters
        ----------
        object (Object):
            The object to add to the time
        """
        self.add_node(object)

    def remove_object(self, object) -> None:
        """
        Removes an object from the time

        Parameters
        ----------
        object (Object):
            The object to remove from the time
        """
        self.remove_node(object)

    def add_thread(self, object1, object2) -> None:
        """
        Adds a thread between two objects
        """
        self.add_edge(object1, object2)

    def remove_thread(self, object1, object2) -> None:
        """
        Removes a thread between two objects
        """
        self.remove_edge(object1, object2)

    def get_state(self, object_id) -> None:
        """
        Returns the state of the object
        """
        return self.nodes[object_id]

    def get_object(self, object_id) -> None:
        """
        Returns the object
        """
        return self.nodes[object_id]

    def draw_time(self) -> None:
        """
        Draws the time
        """
        pass

    def update(self) -> None:
        """
        Updates the object state
        """
        pass
