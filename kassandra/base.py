from _collections_abc import Callable
from typing import Self 

class Base:
    def __init__(self):
        self._update_callback: Callable[[Self], None] | None = None 

    def set_update_callback(self, update_callback: Callable[[Self], None]) -> None:
        self._update_callback = update_callback
