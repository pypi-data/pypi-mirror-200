"""
This module allows you to define specialized classes. This is similar to Generic classes but they are dynamically re-compiled.
Example:

>>> T = TypeVar("T")
>>> @specialize(T)
... class A:
...     def show(param : T):
...         print(T.__name__)
... 
>>> A.show.__annotations__
{'param': ~T}
>>> class B(A[int]):
...     pass
...
>>> B.show.__annotations__
{'param' : <class 'int'>}
>>> B().show()
int
>>> A[int]
<class '__main__.B'>
>>> class C:
...     def show():
...         print("float")
...
>>> A[float] = C        # Registers C as a subclass of A.
"""


def find_me_deco(obj):
    from inspect import getfile, getsource
    print("Found source code of object in", getfile(obj))
    print(getsource(obj))
    return obj