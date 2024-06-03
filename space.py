import networkx as nx


class Space(nx.DiGraph):
    """
    Space class is a directed graph that represents the space of objects.
    It is a subclass of networkx.DiGraph.

    Methods
    -------
    add_object(object):
        Adds an object to the space
    remove_object(object):
        Removes an object from the space
    add_thread(object1, object2):
        Adds a thread between two objects
    remove_thread(object1, object2):
        Removes a thread between two objects
    get_state(object_id):
        Returns the state of the object
    get_object(object_id):
        Returns the object
    draw_space():
        Draws the space
    update():
        Updates the object state
    """

    def __init__(self):
        super().__init__()
        self._input = None
        self._output = None
        self._step = 0
        self._cycle = 0

    def add_object(self, object) -> None:
        """
        Adds an object to the space

        Parameters
        ----------
        object (Object):
            The object to add to the space
        """
        self.add_node(object)

    def remove_object(self, object) -> None:
        """
        Removes an object from the space

        Parameters
        ----------
        object (Object):
            The object to remove from the space
        """
        self.remove_node(object)

    def add_thread(self, object1, object2) -> None:
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

    def remove_thread(self, object1, object2) -> None:
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

    def get_state(self, object_id) -> dict:
        """
        Returns the state of the object

        Parameters
        ----------
        object_id (str):
            The id of the object

        Returns
        -------
        dict:
            The state of the object
        """
        object_node = self.nodes(object_id)
        return dict(object_node)

    def get_object(self, object_id) -> dict:
        """
        Returns the object

        Parameters
        ----------
        object_id (str):
            The id of the object

        Returns
        -------
        dict:
            The object
        """
        return self.nodes(object_id)

    def draw_space(self) -> None:
        nx.draw(self, with_labels=True, font_weight="bold")

    def update(self, input) -> dict:
        """
        Updates the object state

        #! Need to work out inputs and outputs
        #! Need a better counter that different classes can use

        - Iter through every node in the space
        - Update the object
        - Return the state of the object
        - Insert into temporal graph
        - Connect the threads between current state and previous state
        - Finalize update
        - Return the state of the object
        """
        for object in self.nodes:
            object.update()

        return self.state

    @property
    def state(self) -> dict:
        """
        Returns
        -------
        dict:
            The state of the object
        """
        return self.nodes
