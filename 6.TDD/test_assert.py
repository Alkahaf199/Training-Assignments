import pytest

# # Below test failes
# def test_BadFloatCompare():
#     assert (0.1+0.2) == 0.3

def test_GoodFloatCompare():
    val = 0.1+0.2
    assert val == pytest.approx(0.3)

# def test_test1():
#     assert "saumya" == "al kahaf"