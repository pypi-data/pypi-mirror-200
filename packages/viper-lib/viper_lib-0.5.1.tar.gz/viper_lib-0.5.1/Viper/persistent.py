"""
This module adds advanced methods for saving and reloading Python objects or environments.
"""

from typing import Any
from Viper.abc.flux import FluxOperator





class Saver:

    """
    This is used to describe the pickling process of an object. It contains information about:
    - The number of objects (single object, list of objects, Python environment)
    - The FluxOperators applied to it to create the pickle
    """

    def __init__(self, **args_for_flux : Any) -> None:
        from typing import Any
        from Viper.abc.flux import FluxOperator
        self.__flux : list[type[FluxOperator]] = []
        self.__unamed : list[Any] = []
        self.__env : dict[str, Any] = {}
        self.__args : dict[str, Any] = args_for_flux
    
    def __len__(self) -> int:
        """
        Returns the number of objects to be saved.
        """
        return len(self.__unamed) + len(self.__env)
    
    def add_flux(self, f : type[FluxOperator]):
        """
        Adds a flux type in the saving process.
        """
        from Viper.abc.flux import FluxOperator
        if not isinstance(f, type) or not issubclass(f, FluxOperator):
            raise TypeError("Expected FluxOperator, got " + repr(type(f).__name__))
        self.__flux.append(f)

    def append(self, obj : Any):
        """
        Adds an object to be saved.
        """
        self.__unamed.append(obj)
    
    def capture(self):
        """
        Captures the current environment of the caller to be saved.
        """
        from inspect import stack
        self.__env = stack()[1].frame.f_globals.copy()
    
    def dumps(self) -> bytes:
        """
        Executes the saving process of the current content and returns the resulting bytes.
        """
        from inspect import signature
        flux_list = []
        for Flux in self.__flux:
            
            sig = signature(Flux)   # Finding additional parameters for that flux.
            additional_args = {}
            for name, param in sig.parameters:
                if name in self.__args:
                    additional_args[name] = self.__args[name]
            
            flux_list.append(Flux())