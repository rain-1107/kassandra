from .core import BaseObject

class Window(BaseObject):
    def __init__(self) -> None:
        super().__init__()
        self._add_update_callback(Window.update_method) 

    def update_method(self) -> None:
        print("Update")
        pass
