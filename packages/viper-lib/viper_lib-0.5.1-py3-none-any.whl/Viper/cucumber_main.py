from pickle import load
import argparse
from typing import Any
from Viper.format import byte_size
from os.path import getsize
from Viper.interactive import InteractiveInterpreter
import gc


parser = argparse.ArgumentParser(description="Load a Python Type File (.pyt) and lets you manipulate the object in a an interactive shell.")

parser.add_argument("source", type=argparse.FileType("rb"), help="The Python Type File to load an object from.")

args = parser.parse_args()

print("Loading object of {}.".format(byte_size(getsize(args.source.name))))


gc.disable()
obj = load(args.source)
gc.enable()

forbidden_val = object()
def save(value : Any = forbidden_val, destination : str = forbidden_val):
    """
    Saves the given object to the file at given path.
    If called without arguments, will save the object loaded with the current file into the same file. (Saves modifications on the object)
    You can also just give a path to save the current object to another file.
    When saving another object, giving the path is mandatory. (To avoid erasing the original object by mistake)
    """
    if destination is forbidden_val and value is not forbidden_val:
        raise ValueError("If given another object to save, this function requires a destination file.")
    if value is forbidden_val:
        value = obj
    if destination is forbidden_val:
        destination = args.source.name

    from pathlib import Path

    if not isinstance(destination, str | Path):
        raise TypeError("Expected str or Path object, got " + repr(type(destination).__name__))
    
    from pickle import dump
    with open(destination, "wb") as f:
        dump(value, f)


def load(source : str = args.source) -> Any:
    """
    Loads the object stored in file with given path.
    If called without argument, will reload the object that was open in this session.
    """
    from pathlib import Path

    if not isinstance(source, str | Path):
        raise TypeError("Expected str or Path object, got " + repr(type(source).__name__))
    
    from pickle import load
    with open(source, "rb") as f:
        return load(f)
    

           
env = {
    "obj" : obj,
    "save" : save,
    "load" : load
}

InteractiveInterpreter(env).interact("Loaded an object of type '{}' accessible under variable 'obj'.\nUse save() and load() to save and load Python objects.".format(type(obj).__name__))