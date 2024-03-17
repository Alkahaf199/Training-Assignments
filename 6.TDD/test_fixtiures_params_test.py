import pytest 

@pytest.fixture(params=[1,2,3])
def setup(request):
    retval = request.param
    print("\n Setup retval {}".format(retval))
    return retval

def test1(setup):
    print("\nTest = {}".format(setup))
    assert True