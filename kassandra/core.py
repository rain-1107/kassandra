from typing import Self, Callable, List


class BaseObject:
    def __init__(self):
        self._on_ready_callbacks: List[Callable[[Self], None]] = []
        self._on_update_callbacks: List[Callable[[Self], None]] = []
    
    def ready(self):
        for function in self._on_ready_callbacks:
            function(self)

    def update(self):
        for function in self._on_update_callbacks:
            function(self)

    @property
    def on_ready(self):
        def wrapper(function: Callable[[Self], None]):
            if function not in self._on_ready_callbacks:
                self._on_ready_callbacks.append(function)
            return function
        return wrapper
    
    def _add_ready_callback(self, function: Callable[[Self], None]) -> None:
        if function not in self._on_ready_callbacks:
            self._on_ready_callbacks.append(function)

    def _remove_ready_callback(self, function: Callable[[Self], None]) -> None:
        if function in self._on_ready_callbacks:
            self._on_ready_callbacks.remove(function)

    @property
    def on_update(self):
        def wrapper(function: Callable[[Self], None]):
            if function not in self._on_update_callbacks:
                self._on_update_callbacks.append(function)
            return function
        return wrapper

    def _add_update_callback(self, function: Callable[[Self], None]) -> None:
        if function not in self._on_update_callbacks:
            self._on_update_callbacks.append(function)


    def _remove_update_callback(self, function: Callable[[Self], None]) -> None:
        if function in self._on_update_callbacks:
            self._on_update_callbacks.remove(function)
