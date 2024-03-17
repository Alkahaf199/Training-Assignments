from pytest import raises

def raiseValueError():
    # pass
    raise ValueError

def test_exception():
    with raises (ValueError):
        raiseValueError()