from . import jskiner
from . import schema  # noqa: F401


class InferenceEngine:
    def __init__(self, cpu_cnt=1):
        self._engine = jskiner.InferenceEngine(cpu_cnt)

    def run(self, batch):
        exec("from jskiner.schema import *")
        return eval(self._engine.run(batch))

    def reduce(self, schema_list):
        exec("from jskiner.schema import *")
        return eval(self._engine.reduce([s.rc for s in schema_list]))


__doc__ = jskiner.__doc__
if hasattr(jskiner, "__all__"):
    __all__ = jskiner.__all__
    __all__.append("schema")
    __all__.append("InferenceEngine")
