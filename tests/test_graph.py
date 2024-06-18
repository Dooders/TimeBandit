# test_graph.py

import networkx as nx
import pytest

from bandit.graph import Graph


class MockObject:
    def __init__(self, root_id, state):
        self.root_id = root_id
        self.state = state

    def update(self):
        self.state += 1


@pytest.fixture
def setup_graph():
    g = Graph()
    obj1 = MockObject("1", 0)
    obj2 = MockObject("2", 0)
    g.add_object(obj1)
    g.add_object(obj2)
    return g, obj1, obj2


def test_add_object(setup_graph):
    g, obj1, obj2 = setup_graph
    assert g.has_node(obj1.root_id)
    assert g.has_node(obj2.root_id)


def test_remove_object(setup_graph):
    g, obj1, obj2 = setup_graph
    g.remove_object(obj1.root_id)
    assert not g.has_node(obj1.root_id)
    assert g.has_node(obj2.root_id)


def test_get_state(setup_graph):
    g, obj1, obj2 = setup_graph   
    assert obj1.state == 0
    assert obj2.state == 0


def test_get_object(setup_graph):
    g, obj1, _ = setup_graph  # Replace obj2 with _
    obj = g.get_object(obj1.root_id)
    assert obj.state == obj1.state


def test_update(setup_graph):
    g, obj1, obj2 = setup_graph
    g.update()
    assert obj1.state == 1
    assert obj2.state == 1


def test_draw(setup_graph):
    g, _, _ = setup_graph
    g.draw()
    # Visual test - This is difficult to assert but we ensure it doesn't raise an error


def test_objects(setup_graph):
    g, obj1, obj2 = setup_graph
    objects = list(g.objects)
    assert obj1 in objects
    assert obj2 in objects


def test_states(setup_graph):
    g, obj1, obj2 = setup_graph
    states = list(g.states)
    assert obj1.state in states
    assert obj2.state in states


if __name__ == "__main__":
    pytest.main()
