
# Dynamic Memory Allocation in List 

# import sys

# list1 = [1, 2, 'three', 4, 5]
# print(sys.getsizeof(list1))


# def append_into_list(value):
#     print('address: ', id(list1))
#     print('before size of list: ', sys.getsizeof(list1))
#     list1.append(value)
#     print('updated list: ', list1)
#     print('address remains the same: ', id(list1))
#     print('after sizes of list: ', sys.getsizeof(list1))
#     print('')

# append_into_list(6)
# append_into_list(7)
# append_into_list(8)
# append_into_list(9)
# append_into_list(10)
# append_into_list(10)
# append_into_list(10)
# append_into_list(10)
# append_into_list(10)
# append_into_list(11)
# append_into_list(12)
# append_into_list(10)
# append_into_list(11)
# append_into_list(12)
# append_into_list(12)
# append_into_list(10)
# append_into_list(11)
# append_into_list(11)
# append_into_list(11)
# append_into_list(12)
# append_into_list(12)
# append_into_list(12)
# append_into_list(12)
# append_into_list(12)




# Cyclic Refrencing

import ctypes
import gc

# We use ctypes moule  to access our unreachable objects by memory address.
class PyObject(ctypes.Structure):
    _fields_ = [("refcnt", ctypes.c_long)]


gc.disable()  # Disable generational gc

lst = []
lst.append(lst)

# Store address of the list
lst_address = id(lst)

# Destroy the lst reference
del lst

object_1 = {}
object_2 = {}
object_1['obj2'] = object_2
object_2['obj1'] = object_1

obj_address = id(object_1)

# Destroy references
del object_1, object_2

# Uncomment if you want to manually run garbage collection process 
# gc.collect()

# Check the reference count
print(PyObject.from_address(obj_address).refcnt)
print(PyObject.from_address(lst_address).refcnt)
