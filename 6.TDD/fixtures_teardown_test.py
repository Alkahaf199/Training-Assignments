import pytest 

@pytest.fixture()
def setup1():
    print("\nSetup1 !!💀💀💀💀💀💀💀💀")
    yield
    print("Teardown1!!!💀💀💀💀💀💀💀💀\n")

@pytest.fixture()
def setup2(request):
    print("\nSetup2 !!💀💀💀💀💀💀💀💀")

    def teardown_a():
        print("\n Teardown A!!!!")
    
    def teardown_b():
        print("\n Teardwon B????")
    request.addfinalizer(teardown_a)
    request.addfinalizer(teardown_b)

def test1(setup1, setup2):
    print("\n💀💀💀💀💀💀💀💀Test1")

def test2(setup2):
    print("\n💀💀💀💀💀💀💀💀Test2")