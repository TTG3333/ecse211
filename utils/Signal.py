import concurrent.futures

from collections.abc import Callable
from typing import TypeVar, Generic, Dict

T = TypeVar('T')
Callback = Callable[..., None] | None

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
            pool.submit(conn, value)

    def disconnect(self, value):
        self.connections.pop(value, None)