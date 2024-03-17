import pytest 

def setup_function(function):
    if function == test1:
        print("\n Setting up test1")
    elif function == test2:
        print("\n Setting up test2")
    else:
        print("\n Setting up unknown function")
    
def teardown_function(function):
    if function == test1:
        print("\n Tearing down test1")
    elif function == test2:
        print("\n Tearing down test2")
    else:
        print("\n Tearing down unknown function")
    
def test1():
    print("\nExecuting test1")
    assert True

def test2():
    print("\nExecuting Test2")
    assert True