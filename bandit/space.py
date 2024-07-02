"""
The Space module is designed to represent the space of objects in the simulation.

It functions as a directed graph where the edges between objects represent the
Relationships or Interactions between them.

In this design, space is modeled not just as a physical or geometric concept, but as an abstract 
network of connections and influences, where the presence and nature of edges convey the dynamic 
and complex nature of object interactions.

Relationships are specialized types of edges that represent the relationships between
objects in the space.

Interactions are specialized types of edges that represent the interactions between
objects in the space.

Example
-------
Consider a space of objects in a room. The objects are the nodes and the edges
represent the relationships between them.

This example demonstrates how to create a space of objects in a "room" and represent 
their relationships as edges in a graph.

1. Create instances of objects that represent items in the room.
2. Add these objects as nodes to the Space graph.
3. Define relationships (edges) between these objects to represent their 
    interactions or spatial relations.
4. Utilize the Space graph to analyze or visualize the relationships and 
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

    # Define relationships
    room_space.add_relationship(chair, table, relationship="next to")
    room_space.add_relationship(table, lamp, relationship="under")

    # Visualize the objects and relationships
    room_space.draw()
    
TODO
----
- Build out Relationship and Interaction edges
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
    add_relationship(object1, object2, relationship)
        Add a relationship between two objects.
    remove_relationship(object1, object2)
        Remove a relationship between two objects.
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

    def add_relationship(
        self, object1: "Object", object2: "Object", relationship: str
    ) -> None:
        """
        Add a relationship between two objects.

        Parameters
        ----------
        object1 : Object
            The first object in the relationship.
        object2 : Object
            The second object in the relationship.
        relationship : str
            The type of relationship between the two objects.
        """
        self.add_edge(object1, object2, relationship=relationship)

    def remove_relationship(self, object1: "Object", object2: "Object") -> None:
        """
        Remove a relationship between two objects.
        """
        self.remove_edge(object1, object2)

    def add_interaction(
        self, object1: "Object", object2: "Object", interaction: str
    ) -> None:
        """
        Add an interaction between two objects.
        """
        self.add_edge(object1, object2, interaction=interaction)

    def remove_interaction(self, object1: "Object", object2: "Object") -> None:
        """
        Remove an interaction between two objects.
        """
        self.remove_edge(object1, object2)

    @property
    def relationships(self) -> list[tuple[str, str, str]]:
        """
        Return a list of relationships in the space.
        """
        return [(u, v, d["relationship"]) for u, v, d in self.edges.data()]

    @property
    def interactions(self) -> list[tuple[str, str, str]]:
        """
        Return a list of interactions in the space.
        """
        return [(u, v, d["interaction"]) for u, v, d in self.edges.data()]

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
