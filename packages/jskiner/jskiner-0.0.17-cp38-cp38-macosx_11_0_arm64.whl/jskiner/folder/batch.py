from typing import Iterable
from typing import List
from typing import Any


class Batcher:
    def __init__(self, batch_size=10000):
        self._batch_size = batch_size

    def connect(self, input_generator: Iterable[Any]) -> Iterable[List[Any]]:
        batch = []
        for i, element in enumerate(input_generator):
            batch.append(element)
            if i % self._batch_size == (self._batch_size - 1):
                yield batch
                del batch
                batch = []
        if batch:
            yield batch
