# test_graph.py

import pytest

from bandit.graph import Graph
from bandit.object import Object


@pytest.fixture
def setup_graph():
    g = Graph()
    obj1 = Object()
    obj2 = Object()
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
    g, obj1, _ = setup_graph  # Replace obj2 with _
    obj = g.get_object(obj1.id.root)
    assert obj.state == obj1.state


def test_update(setup_graph):
    g, obj1, obj2 = setup_graph
    g.update()
    assert obj1.state == 1
    assert obj2.state == 1


def test_draw(setup_graph):
    g, _, _ = setup_graph
    g.draw()


def test_objects(setup_graph):
    g, obj1, obj2 = setup_graph
    objects = list(g.objects)
    assert obj1 in objects
    assert obj2 in objects
