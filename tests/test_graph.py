# test_graph.py

import pytest

from bandit.graph import Graph
from bandit.object import Object


class MockGraph(Graph):
    def __init__(self):
        super().__init__()

    def _update(self):
        print("update")


class MockObject(Object):
    def __init__(self):
        super().__init__()

    def _update(self):
        print("update")


@pytest.fixture
def setup_graph():
    g = MockGraph()
    obj1 = MockObject()
    obj2 = MockObject()
    g.add_object(obj1)
    g.add_object(obj2)
    return g, obj1, obj2


def test_add_object(setup_graph):
    g, obj1, obj2 = setup_graph
    assert g.has_node(obj1.id.root)
    assert g.has_node(obj2.id.root)


def test_remove_object(setup_graph):
    g, obj1, obj2 = setup_graph
    g.remove_object(obj1)
    assert not g.has_node(obj1.id.root)
    assert g.has_node(obj2.id.root)


def test_get_object(setup_graph):
    g, obj1, _ = setup_graph
    obj = g.get_object(obj1.id.root)
    assert obj.state == obj1.state


def test_update(setup_graph):
    g, obj1, obj2 = setup_graph
    assert obj1.state()["cycle"] == 1
    assert obj2.state()["cycle"] == 1
    g.update()
    assert obj1.state()["cycle"] == 2
    assert obj2.state()["cycle"] == 2


def test_objects(setup_graph):
    g, obj1, obj2 = setup_graph
    objects = list(g.objects)
    assert obj1 in objects
    assert obj2 in objects


def test_state(setup_graph):
    g, obj1, obj2 = setup_graph
    graph_state = g.state
    assert len(graph_state) == 2
    assert graph_state["object_states"] == {}
    g.update()
    graph_state = g.state
    assert len(graph_state["object_states"]) == 2
