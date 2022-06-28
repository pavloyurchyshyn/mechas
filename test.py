import os
import importlib
import inspect
from mechas.base.mech import BaseMech

from mechas import details

#print(inspect.getmembers(details))
for v in inspect.getmembers(details, inspect.isclass):
    if not issubclass(v[1], BaseMech):
        print(v)