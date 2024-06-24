from bandit.clock import Clock
from bandit.identity import Identity


def test_identity():
    identity = Identity()
    assert type(identity.root) == str
    assert identity.temporal == f"{identity.root}.1.0"


def test_identity_update():
    identity = Identity()
    clock = Clock()
    identity.update(clock)
    assert identity.temporal == f"{identity.root}.{clock.cycle}.{clock.step}"


def test_identity_call():
    identity = Identity()
    assert identity() == identity.temporal
    assert identity(root=True) == identity.root
