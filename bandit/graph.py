"""
Graph class is a abstract class that represents a graph.

It is a subclass of networkx.DiGraph.

A graph is a collection of nodes and edges. The nodes are the objects in the graph
and the edges are the relationships between the objects.

It is intended to be subclassed by concrete implementations of graphs. Like
the Space class and the Time class.
    
TODO
----
- Better state management to auto use parent state details so dont have to 
    define with every child
- Investigate if class should inherit from Object that way it has a state, 
    clock, _update, etc
- Investigate if class should also be a Graph Neural Network
"""

from abc import abstractmethod
from typing import TYPE_CHECKING, Generator

import networkx as nx

from bandit.state import State

if TYPE_CHECKING:
    from bandit.object import Object


class Graph(nx.DiGraph):
    """
    Graph class is a abstract class that represents a graph.

    It is a subclass of networkx.DiGraph.

    It is intended to be subclassed by concrete implementations of graphs. Like
    the Space class and the Time class.

    Methods
    -------
    add_object(object):
        Adds an object to the space
    remove_object(object):
        Removes an object from the space
    get_object(object_id):
        Returns the object
    update(input):
        Updates the object state
    draw():
        Draws the graph

    Properties
    ----------
    objects: Generator["Object", None, None]
        Returns a generator of objects in the graph
    state: dict
        Returns the current state of the graph
    """

    def __init__(self) -> None:
        super().__init__()
        self.object_states = {}

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

    def get_object(self, object_id) -> "Object":
        """
        Returns the object

        Parameters
        ----------
        object_id (str):
            The id of the object

        Returns
        -------
        Object:
            The object
        """
        return self.nodes[object_id]["object"]

    @abstractmethod
    def _update(self) -> None:
        """
        Updates the object state

        """
        raise NotImplementedError("Subclass must implement _update")

    def update(self) -> dict:
        """
        Updates the object state

        Iterates through every object in the graph and updates their state.

        Returns the state of the graph.

        TODO
        ----
        - Optimize this process
        """
        self.object_states = {}
        for object in self.objects:
            # Update every object in the graph
            self.object_states[object.root_id] = object.update()

        return self.state

    def draw(self) -> None:
        """
        Draws the graph
        """
        nx.draw(self, with_labels=True, font_weight="bold")

    @property
    def objects(self) -> Generator["Object", None, None]:
        """
        Returns the objects in the graph
        """
        for node in self.nodes():
            yield self.nodes[node]["object"]

    @property
    def state(self) -> "State":
        """
        Returns the state of the graph
        """
        return State(
            {
                "object_count": len(self.object_states),
                "object_states": self.object_states,
            }
        )
