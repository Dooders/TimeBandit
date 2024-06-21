# test_state.py
import pytest
from bandit.state import State

def test_state():
    state = State({"a": 1, "b": 2})
    assert state["a"] == 1
    assert state["b"] == 2  
    
