import concurrent.futures

from collections.abc import Callable
from typing import TypeVar, Generic, Dict, Optional

T = TypeVar('T')
Callback = Optional[Callable[..., None]]

pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

class Signal(Generic[T]):
    def __init__(self):
        self.id = -1
        self.connections: Dict[int, Callback] = {}

    def connect(self, callback: Callback):
        self.id += 1
        self.connections[self.id] = callback
        return self.id

    def fire(self, value: T):
        for conn in self.connections.values():
            if conn is not None:
                pool.submit(conn, value)

    def disconnect(self, value: int):
        self.connections.pop(value, None)