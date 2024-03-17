import pytest

def fizzBuzz(str):
    return len(str)

def test_canCallFizzBuzz():
    eval  = "hell"
    result = fizzBuzz(eval)
    assert result == 4
