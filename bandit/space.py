"""
The Space module is designed to represent the space of objects in the simulation.

It functions as a directed graph where the edges between objects represent the
Relationships or Interactions between them.

In this design, space is modeled not just as a physical or geometric concept, but as an abstract 
network of connections and influences, where the presence and nature of edges convey the dynamic 
and complex nature of object interactions.

Connections are specialized types of edges that represent the connections between
objects in the space.

Interactions are specialized types of edges that represent the interactions between
objects in the space.

Example
-------
Consider a space of objects in a room. The objects are the nodes and the edges
represent the connections between them.

This example demonstrates how to create a space of objects in a "room" and represent 
their connections as edges in a graph.

1. Create instances of objects that represent items in the room.
2. Add these objects as nodes to the Space graph.
3. Define connections (edges) between these objects to represent their 
    interactions or spatial relations.
4. Utilize the Space graph to analyze or visualize the connections and 
    interactions between objects.

    # Create a space
    room_space = Space()

    # Define some objects
    chair = Object(name="Chair")
    table = Object(name="Table")
    lamp = Object(name="Lamp")

    # Add objects to the space
    room_space.add_object(chair)
    room_space.add_object(table)
    room_space.add_object(lamp)

    # Define connections
    room_space.add_connection(chair, table, connection="next to")
    room_space.add_connection(table, lamp, connection="under")

    # Visualize the objects and connections
    room_space.draw()
    
TODO
----
- Build out Connection and Interaction edges
- Add methods to Space for getting the state of the space
- Loading a Space from a SpaceState
- Tests
"""

from typing import TYPE_CHECKING

from bandit.graph import Graph
from bandit.state import State

if TYPE_CHECKING:
    from bandit.object import Object


class Space(Graph):
    """
    Space class is a directed graph that represents the space of objects (nodes).

    It is a subclass of networkx.DiGraph.

    Methods
    -------
    add_connection(object1, object2, connection)
        Add a connection between two objects.
    remove_connection(object1, object2)
        Remove a connection between two objects.
    add_interaction(object1, object2, interaction)
        Add an interaction between two objects.
    remove_interaction(object1, object2)
        Remove an interaction between two objects.
    object_count
        Return the number of objects in the space.
    state
        Return the state of the space and the state of the objects in the space
    """

    def __init__(self) -> None:
        super().__init__()

    def add_connection(
        self, object1: "Object", object2: "Object", connection: str
    ) -> None:
        """
        Add a connection between two objects.

        Parameters
        ----------
        object1 : Object
            The first object in the connection.
        object2 : Object
            The second object in the connection.
        connection : str
            The type of connection between the two objects.
        """
        object1.connections.add(object2.id.root, object2, connection)

    def remove_connection(self, object1: "Object", object2: "Object") -> None:
        """
        Remove a connection between two objects.
        """
        object1.connections.remove(object2.id.root)

    def add_interaction(
        self, object1: "Object", object2: "Object", interaction: str
    ) -> None:
        """
        Add an interaction between two objects.
        """
        object1.interactions.add(object2.id.root, object2, interaction)

    def remove_interaction(self, object1: "Object", object2: "Object") -> None:
        """
        Remove an interaction between two objects.
        """
        object1.interactions.remove(object2.id.root)

    @property
    def connections(self) -> list[tuple[str, str, str]]:
        """
        Iterate over every object in the space and return a list of connections
        """
        return [x.connections for x in self.objects if x.connections]

    @property
    def interactions(self) -> list[tuple[str, str, str]]:
        """
        Return a list of interactions in the space.
        """
        return [x.interactions for x in self.objects if x.interactions]

    @property
    def object_count(self) -> int:
        """
        Return the number of objects in the space.
        """
        return len(self.nodes)

    @property
    def state(self) -> State:
        """
        Return the state of the space and the state of the objects in the space
        """
        return State(
            {
                "object_count": self.object_count,
                "objects": {node: node.state for node in self.objects},
            }
        )
