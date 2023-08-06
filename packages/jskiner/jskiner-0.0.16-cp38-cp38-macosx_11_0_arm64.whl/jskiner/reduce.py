from typing import Iterable

exec("from .schema import *")


class SchemaReducer:
    def __init__(self, schema_str="Unknown()"):
        self._schema = eval(schema_str)

    def reduce(self, schema_string_generator: Iterable[str]) -> str:
        try:
            for schema_string in schema_string_generator:
                self._schema |= eval(schema_string)
            return self._schema.__repr__()
        except BaseException as e:
            print("Error on:\n", schema_string)
            raise e
