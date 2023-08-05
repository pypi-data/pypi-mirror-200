"""
This module adds metaclasses that make a class a statically-typed class.
For such a class, all of its methods would first check if their arguments match the type annotations when called.
Note that no annotations is equivalent to Typing.Any, except for:
    - self (first argument) of normal methods will be interpreted as an instance of the class.
    - cls (first argument) of class methods will be interpreted as the class itself or one of its subclasses.
"""


from typing import Any, Callable, Dict, FrozenSet, List, Set, Type, Tuple, TypeVar, Union
from .iterable import InstancePreservingClass






class TypeChecker(metaclass = InstancePreservingClass):

    """
    This class lets you describe a way to handle statically a type.
    """

    __slots__ = {
        "matcher" : "A function that should tell if a given type should be handled by this TypeChecker",
        "checker" : "The checker function, that should tell if an object is an instance of the class it is the TypeChecker of",
        "_explanation" : "A string describing the type that the TypeChecker is handling"
    }

    def __init__(self, matcher : Callable[[type], bool], checker : Callable[[Any, type], bool], explanation : str | Callable[[type], str]) -> None:
        if not callable(matcher) or not callable(checker) or (not isinstance(explanation, str) and not callable(explanation)):
            raise TypeError("Expected callable, callable, str, got " + repr(matcher.__class__.__name__) + ", " + repr(checker.__class__.__name__) + " and " + repr(explanation.__class__.__name__))
        
        self.matcher = matcher
        self.checker = checker
        self._explanation = explanation
    
    def explanation(self, t : type = object) -> str:
        if isinstance(self._explanation, str):
            return self._explanation
        else:
            return self._explanation(t)

    def __contains__(self, t : type) -> bool:
        return self.matcher(t)

    def match(self, t : type) -> bool:
        return t in self
    
    def __call__(self, o : Any, t : type) -> bool:
        return self.checker(o, t)
    
    def check(self, o : Any, t : type) -> bool:
        return self(o, t)




def find_or_create_type_checker(t : type) -> TypeChecker:
    tc : TypeChecker
    for tc in TypeChecker:
        if t in tc:
            return tc
    return TypeChecker(lambda o : o == t, lambda o, t : isinstance(o, t), t.__name__)




CLS = TypeVar("CLS")

class StaticTypedClass(type):

    def __new__(cls : Type[CLS], name : str, bases : Tuple[type], dct : dict):
        """
        Implements the creation of a new class
        """

        from inspect import signature, Signature, Parameter, _empty
        from typing import Callable, Union, Dict, Any, List
        
        
        future_changes : List[dict] = []
        
        
        namespace : Dict[str, Any] = {}
        translation_table : Dict[type | TypeChecker, str] = {}



        def instance_checker(name : str, t : type) -> str:
            """
            This function should return an executable expression answering whether or not variable "name" host a value of type t.
            """
            
            tc = find_or_create_type_checker(t)
            if tc in translation_table:
                tcname = translation_table[tc]
            else:
                tcname = new_var("type_checker")
                namespace[tcname] = tc
                translation_table[tc] = tcname
            if t in translation_table:
                tname = translation_table[t]
            else:
                tname = new_var(t.__name__ if hasattr(t, "__name__") else "type_var")
                namespace[tname] = t
                translation_table[t] = tname
            return "{}({}, {})".format(tcname, name, tname)


        def type_format(t : type) -> str:
            """
            Returns an explanation string for the type t.
            """

            tc = find_or_create_type_checker(t)
            return tc.explanation(t)
            
            if type(t) in (type(Union[int, str]), type(int | str)):
                return ", ".join(type_format(ti) for ti in t.__args__[:-1]) + " or " + type_format(t.__args__[-1])
            if t == type(None):
                return "None"
        

        def type_converter(t : type) -> type:
            """
            Returns a proper value to use for type checking.
            """
            if t == Signature.empty:
                return None
            if t == None:
                return type(None)
            return t
        

        def new_var(prefix : str) -> str:
            """
            Generates a new variable name for the code being redacted.
            """
            if prefix not in namespace:
                namespace[prefix] = None
                return prefix
            i = 1
            while prefix + "_" + str(i) in namespace:
                i += 1
            name = prefix + "_" + str(i)
            namespace[name] = None
            return name


        def wrapper(f : Callable) -> Callable:
            """
            Creates a wrapper function to handle the type checking of all kinds of methods.
            This will actually start writing some function code and execute the declaration.
            """

            ## Discovering the function

            method = isinstance(f, type(StaticTypedClass.__new__))
            clsmethod = isinstance(f, classmethod)
            statmethod = isinstance(f, staticmethod)

            ## Property wrapper

            if isinstance(f, property):
                if f.fset:
                    f.setter(wrapper(f.fset))
                if f.fget:
                    f.getter(wrapper(f.fget))
                if f.fdel:
                    f.deleter(wrapper(f.fdel))
                return f

            ## Extracting function name

            if clsmethod or statmethod:
                f = f.__func__
            
            ## Initialization of namespace

            sig = signature(f)
            namespace.update({n : None for n in sig.parameters})
            namespace["original_" + f.__name__] = f
            namespace[f.__name__] = None
            future_class = type(name, (), {})
            namespace[name] = future_class
            translation_table[future_class] = name

            ## Redacting a copy of the signature, with new variables for annotations and defaults

            abstract_sig = "("

            arg_levels = {
                Parameter.POSITIONAL_ONLY : 0,
                Parameter.POSITIONAL_OR_KEYWORD : 1,
                Parameter.VAR_POSITIONAL : 2,
                Parameter.KEYWORD_ONLY : 3,
                Parameter.VAR_KEYWORD : 4
            }
            arg_numbers = [0, 0, 0, 0, 0]
            arg_level = 0

            done = False

            for i, (pname, param) in enumerate(sig.parameters.items()):
                if arg_level != arg_levels[param.kind]:
                    if arg_levels[param.kind] > arg_levels[Parameter.POSITIONAL_ONLY] and arg_numbers[Parameter.POSITIONAL_ONLY] and not done:
                        abstract_sig += "/, "
                        done = True
                    if param.kind == Parameter.KEYWORD_ONLY and arg_numbers[Parameter.VAR_POSITIONAL] == 0:
                        abstract_sig += "*, "
                    arg_level = arg_levels[param.kind]
                arg_numbers[arg_level] += 1
                if param.kind == Parameter.VAR_POSITIONAL:
                    abstract_sig += "*"
                if param.kind == Parameter.VAR_KEYWORD:
                    abstract_sig += "**"
                abstract_sig += pname
                if param.annotation != _empty:
                    type_var = new_var("type_var")
                    namespace[type_var] = param.annotation
                    abstract_sig += " : " + type_var
                if param.default != _empty:
                    default_var = new_var("default_var")
                    namespace[default_var] = param.default
                    abstract_sig += " = " + default_var
                if i + 1 < len(sig.parameters):
                    abstract_sig += ", "
            
            abstract_sig += ")"

            if sig.return_annotation:
                ret_var = new_var("return_var")
                namespace[ret_var] = sig.return_annotation
                abstract_sig += " -> " + ret_var

            code = """
def {}{}:
""".format(f.__name__, abstract_sig)

            ## Copying the function documentation

            if f.__doc__:
                code += """
    '''{}'''
""".format(f.__doc__)

            ## Referencing globals

            code += """
    global original_{}
""".format(f.__name__)

            ## Writing down all of the type checkers (for each argument)

            for i, (pname, param) in enumerate(sig.parameters.items()):
                ntype = type_converter(param.annotation)
                if method and i == 0:
                    ntype = future_class
                    future_changes.append(namespace)
                if clsmethod and i == 0:
                    ntype = cls
                if ntype == None:        # No type annotation (or Any) -> skip type check
                    continue
                if param.kind == param.VAR_POSITIONAL:
                    loop_var = new_var(pname + "_i")
                    code += """
    for {} in {}:
        if not ({}):
            raise TypeError("Expected {} for {}, got " + repr({}.__class__.__name__))
""".format(loop_var, pname, instance_checker(loop_var, ntype), type_format(ntype), pname, loop_var)

                elif param.kind == param.VAR_KEYWORD:
                    loop_var = new_var(pname + "_i")
                    code += """
    for {} in {}.values():
        if not ({}):
            raise TypeError("Expected {} for {}, got " + repr({}.__class__.__name__))
""".format(loop_var, pname, instance_checker(loop_var, ntype), type_format(ntype), pname, loop_var)

                else:
                    code += """
    if not ({}):
        raise TypeError("Expected {} for {}, got " + repr({}.__class__.__name__))
""".format(instance_checker(pname, ntype), type_format(ntype), pname, pname)
            
            ## Making the call to the original function

            arguments = [[], [], [], [], []]
            for pname, arg in sig.parameters.items():
                if arg.kind == arg.POSITIONAL_ONLY:
                    arguments[0].append(pname)
                elif arg.kind == arg.POSITIONAL_OR_KEYWORD:
                    arguments[1].append(pname)
                elif arg.kind == arg.VAR_POSITIONAL:
                    arguments[2].append("*" + pname)
                elif arg.kind == arg.KEYWORD_ONLY:
                    arguments[3].append(pname + "=" + pname)
                elif arg.kind == arg.VAR_KEYWORD:
                    arguments[4].append("**" + pname)
                                    
            i = 0
            while i < len(arguments):
                if not arguments[i]:
                    arguments.pop(i)
                else:
                    i += 1

            call = "(" + ", ".join(", ".join(argij for argij in argi) for argi in arguments) + ")"

            code += """
    result = original_{}{}
""".format(f.__name__, call)

            ## Checking the type of the result

            if type_converter(sig.return_annotation) != None:
                code += """
    if not ({}):
        raise TypeError("Function {} did not return {}.")
""".format(instance_checker("result", type_converter(sig.return_annotation)), f.__name__, type_format(type_converter(sig.return_annotation)))
            
            code += """
    return result"""

            ## "Compiling" statically-typed function

            exec(code, namespace)

            # print("### BEGIN NAMESPACE ###")
            # for pname, val in namespace.items():
            #     if pname != "__builtins__":
            #         print(pname, "=", val)
            # print("### BEGIN CODE ###")
            # print(code)
            # print("### END ###\n\n")

            ## Retrieving the resulting function

            func = namespace[f.__name__]

            ## Recasting if necessary

            if clsmethod:
                func = classmethod(func)
            if statmethod:
                func = staticmethod(func)
            
            ## Finished

            return func





        for aname, attr in dct.items():
            if isinstance(attr, type(StaticTypedClass.__new__)) or isinstance(attr, classmethod) or isinstance(attr, staticmethod) or isinstance(attr, property):
                namespace = {}
                translation_table = {}
                dct[aname] = wrapper(attr)
        newcls = super().__new__(cls, name, bases, dct)

        for namespace in future_changes:
            namespace[name] = newcls

        return newcls







## Defining basic TypeCheckers

TypeChecker(lambda t : t == None, lambda o, t : isinstance(o, type(t)), "None")
TypeChecker(lambda t : isinstance(t, (type(int | str), type(Union[int, str]))), lambda o, t : any(find_or_create_type_checker(ti)(o, ti) for ti in t.__args__), lambda t : " or ".join(find_or_create_type_checker(ti).explanation(ti) for ti in t.__args__))
TypeChecker(lambda t : isinstance(t, (type(List[int]), type(list[int]))) and t.__origin__ == list, lambda o, t : isinstance(o, list) and all(find_or_create_type_checker(t.__args__[0])(oi, t.__args__[0]) for oi in o), lambda t : "list of " + find_or_create_type_checker(t.__args__[0]).explanation(t.__args__[0]))
TypeChecker(lambda t : isinstance(t, (type(Set[int]), type(set[int]))) and t.__origin__ == set, lambda o, t : isinstance(o, set) and all(find_or_create_type_checker(t.__args__[0])(oi, t.__args__[0]) for oi in o), lambda t : "set of " + find_or_create_type_checker(t.__args__[0]).explanation(t.__args__[0]))
TypeChecker(lambda t : isinstance(t, ((type(FrozenSet[int])), type(frozenset[int]))) and t.__origin__ == frozenset, lambda o, t : isinstance(o, frozenset) and all(find_or_create_type_checker(t.__args__[0])(oi, t.__args__[0]) for oi in o), lambda t : "frozenset of " + find_or_create_type_checker(t.__args__[0]).explanation(t.__args__[0]))
TypeChecker(lambda t : isinstance(t, ((type(Dict[int, int])), type(dict[int, int]))) and t.__origin__ == dict, lambda o, t : isinstance(o, dict) and all(find_or_create_type_checker(t.__args__[0])(ki, t.__args__[0]) and find_or_create_type_checker(t.__args__[1])(vi, t.__args__[1]) for ki, vi in o.items()), lambda t : "dict of " + find_or_create_type_checker(t.__args__[0]).explanation(t.__args__[0]) + " to " + find_or_create_type_checker(t.__args__[1]).explanation(t.__args__[1]))
TypeChecker(lambda t : isinstance(t, (type(Tuple[int]), type(tuple[int]))) and t.__origin__ == tuple, lambda o, t : isinstance(o, tuple) and ((all(find_or_create_type_checker(t.__args__[0])(oi, t.__args__[0]) for oi in o)) if (len(t.__args__) == 2 and t.__args__[1] == ...) else (len(o) == len(t.__args__) and all(find_or_create_type_checker(t.__args__[i])(o[i], t.__args__[i]) for i in range(len(o))))), lambda o, t : "tuple of " + (("multiple " + find_or_create_type_checker(t.__args__[0]).explanation(t.__args__[0])) if (len(t.__args__) == 2 and t.__args__[1] == ...) else (", ".join(find_or_create_type_checker(ti).explanation(ti) for ti in t.__args__[:-1]) + (" and " * (bool(len(t.__args__) > 1))) + find_or_create_type_checker(t.__args__[-1]).explanation(t.__args__[-1]))))
