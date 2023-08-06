from . import jskiner  # noqa: F401

schema_names = [
    "Int",
    "Float",
    "Str",
    "Non",
    "Bool",
    "Atomic",
    "Array",
    "Record",
    "FieldSet",
    "UniformRecord",
    "Union",
    "Optional",
    "Unknown",
]


def convert_py_2_rust(arg):
    if isinstance(arg, dict):
        arg = dict([(key, value.rc) for key, value in arg.items()])
    elif isinstance(arg, set):
        arg = set([e.rc for e in arg])
    else:
        arg = arg.rc
    return arg


def code_gen(class_name):
    """
    Arg:
        - class_name: The name of the python schema class
    Return:
        - class_define_code: Python code defining a python class that
            warps the schema class defined in lib.rs into pure python
            schema object.
    """
    class_define_code = f"""
class {class_name}:
    def __init__(self, *args):
        if len(args) == 1:
            if '{class_name}' == 'FieldSet':
                self.rc = jskiner.{class_name}(args[0])
            else:
                self.rc = jskiner.{class_name}(convert_py_2_rust(args[0]))
        elif len(args) == 2:
            self.rc = jskiner.{class_name}(convert_py_2_rust(args[0]), convert_py_2_rust(args[1]))
        else:
            self.rc = jskiner.{class_name}()
    def __repr__(self):
        return str(self.rc)
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()
    def __hash__(self):
        return hash(self.__repr__())
    def __or__(self, other):
        engine = jskiner.InferenceEngine(1)
        return eval(engine.reduce([self.rc, other.rc]))
"""
    return class_define_code


for class_name in schema_names:
    exec(code_gen(class_name))

__all__ = schema_names
