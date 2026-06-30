from dataclasses import dataclass

@dataclass
class FunctionInfo:
    name:str
    args:list
    returns:str|None
    decorators:list
    docstring:str|None
    start_line:int
    end_line:int

@dataclass
class ClassInfo:
    name:str
    bases:list
    decorators:list
    docstring:str|None
    methods:list

@dataclass
class FileInfo:
    path:str
    imports:list
    functions:list
    classes:list
    calls:list
