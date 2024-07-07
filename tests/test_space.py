import pytest

from bandit.object import Object
from bandit.space import Space


@pytest.fixture
def space():
    return Space()


@pytest.fixture
def objects():
    return [Object() for i in range(3)]


def test_add_object(space, objects):
    for obj in objects:
        space.add_object(obj)
    assert space.object_count == 3


def test_add_connection(space, objects):
    obj1, obj2, obj3 = objects
    space.add_object(obj1)
    space.add_object(obj2)
    space.add_object(obj3)
    space.add_connection(obj1, obj2, "next to")
    space.add_connection(obj2, obj3, "under")
    assert len(space.connections) == 2


def test_remove_connection(space, objects):
    obj1, obj2 = objects[:2]
    space.add_object(obj1)
    space.add_object(obj2)
    space.add_connection(obj1, obj2, "next to")
    space.remove_connection(obj1, obj2)
    assert len(space.connections) == 0


def test_add_interaction(space, objects):
    obj1, obj2, obj3 = objects
    space.add_object(obj1)
    space.add_object(obj2)
    space.add_object(obj3)
    space.add_interaction(obj1, obj2, "push")
    space.add_interaction(obj2, obj3, "pull")
    assert len(space.interactions) == 2


def test_remove_interaction(space, objects):
    obj1, obj2 = objects[:2]
    space.add_object(obj1)
    space.add_object(obj2)
    space.add_interaction(obj1, obj2, "push")
    space.remove_interaction(obj1, obj2)
    assert len(space.interactions) == 0


def test_object_count(space, objects):
    for obj in objects:
        space.add_object(obj)
    assert space.object_count == 3


def test_state(space, objects):
    for obj in objects:
        space.add_object(obj)
    state = space.state
    assert state["object_count"] == 3
    assert "objects" in state
