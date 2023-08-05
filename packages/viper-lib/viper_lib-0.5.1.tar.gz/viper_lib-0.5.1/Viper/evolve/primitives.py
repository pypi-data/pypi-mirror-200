"""

"""

import ast





class Editor:

    """
    This class allows you to write executable Python code. It can then be compiled and executed.
    """

    def __init__(self, src : ast.AST | str | None = None) -> None:
        import ast
        if src != None and not isinstance(src, ast.AST | str):
            raise TypeError("Expected executable code or Abstract Syntax Tree, got " + repr(type(src).__name__))
        if src == None:
            self.__src = ast.Module()
        elif isinstance(src, str):
            try:
                self.__src = ast.parse(src, "<edited string>", "exec")
            except SyntaxError as E:
                raise E from None
        else:
            self.__src = src
        self.__current_node : ast.AST = self.__src
        self.__stackframe : list[ast.AST] = []
    
    

    def names()