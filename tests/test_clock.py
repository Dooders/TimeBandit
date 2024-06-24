import time
from bandit.clock import Clock


def test_clock_update():
    clock = Clock(10)
    assert clock.time == "1:0"
    clock.update()
    assert clock.time == "1:1"
    clock.update()
    assert clock.time == "1:2"
    clock.update()
    assert clock.time == "1:3"


def test_clock_reset():
    clock = Clock(10)
    clock.update()
    clock.reset()
    assert clock.time == "1:0"


def test_clock_clone():
    clock = Clock(10)
    clock.update()
    clock.update()
    clock.update()
    clock.update()
    assert clock.time == "1:4"
    clock2 = clock.clone()
    assert clock2.time == "1:4"


def test_clock_real_time():
    clock = Clock(10)
    assert clock.real_time == 0
    time.sleep(1)
    assert clock.real_time > 0