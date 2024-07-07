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


def test_clock_max_value():
    clock = Clock(10)
    for _ in range(10):
        clock.update()
    assert clock.time == "2:0"


def test_clock_multiple_updates():
    clock = Clock(10)
    for _ in range(5):
        clock.update()
    assert clock.time == "1:5"
    for _ in range(5):
        clock.update()
    assert clock.time == "2:0"


def test_clock_real_time_multiple_updates():
    clock = Clock(10)
    initial_real_time = clock.real_time
    time.sleep(1)
    clock.update()
    assert clock.real_time > initial_real_time
    time.sleep(1)
    clock.update()
    assert clock.real_time > initial_real_time + 1
