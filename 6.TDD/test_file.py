import pytest

# @pytest.fixture()

# For every test to run text fixture
@pytest.fixture(autouse=True)
def mysetup():
    print("\nSetup")

def test1():
    print("\nExecuting test1")
    assert True

# To call particula text fixtures
# @pytest.mark.usefixtures("setup") 
    
def test2():
    print("\nExecuting test2")
    assert True