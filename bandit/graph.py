import networkx as nx


class Graph(nx.DiGraph):
    """
    Space class is a directed graph that represents the space of objects.
    It is a subclass of networkx.DiGraph.

    Methods
    -------
    add_object(object):
        Adds an object to the space
    remove_object(object):
        Removes an object from the space
    get_state(object_id):
        Returns the state of the object
    get_object(object_id):
        Returns the object
    draw_space():
        Draws the space
    update(input):
        Updates the object state
    draw():
        Draws the graph
    """

    def __init__(self) -> None:
        super().__init__()

    def add_object(self, object) -> None:
        """
        Adds an object to the space

        Parameters
        ----------
        object (Object):
            The object to add to the space
        """
        self.add_node(object.root_id, object=object)

    def remove_object(self, object) -> None:
        """
        Removes an object from the space

        Parameters
        ----------
        object (Object):
            The object to remove from the space
        """
        self.remove_node(object)

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

    def update(self) -> dict:
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

    def draw(self) -> None:
        """
        Draws the graph
        """
        nx.draw(self, with_labels=True, font_weight="bold")

    @property
    def objects(self) -> dict:
        """
        Returns the objects in the graph
        """
        for node in self.nodes():
            yield self.nodes[node]["object"]

    @property
    def states(self) -> dict:
        """
        Returns
        -------
        dict:
            The state of the object
        """
        for object in self.objects:
            yield object.state
