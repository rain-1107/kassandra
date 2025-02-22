from typing import Self, Callable, List, Tuple
import typing

FVectorLike = typing.Union[List[float], Tuple[float, float]]
IVectorLike = typing.Union[List[int], Tuple[int, int]]
Matrix2x2Like = typing.Union[List[List[float]], Tuple[Tuple[float, float], 
                                                      Tuple[float, float]]]
Matrix3x3Like = typing.Union[List[List[float]], Tuple[Tuple[float, float, float], 
                                                      Tuple[float, float, float], 
                                                      Tuple[float, float, float]]]
Matrix4x4Like = typing.Union[List[List[float]], Tuple[Tuple[float, float, float, float], 
                                                      Tuple[float, float, float, float], 
                                                      Tuple[float, float, float, float], 
                                                      Tuple[float, float, float, float]]]

def flatten_mat2x2(matrix: Matrix2x2Like) -> List[float]:
    return [matrix[0][0], matrix[0][1],
            matrix[1][0], matrix[1][1]]


def flatten_mat3x3(matrix: Matrix3x3Like) -> List[float]:
    return [matrix[0][0], matrix[0][1], matrix[0][2],
            matrix[1][0], matrix[1][1], matrix[1][2],
            matrix[2][0], matrix[2][1], matrix[2][2]]


def flatten_mat4x4(matrix: Matrix4x4Like) -> List[float]:
    return [matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3],
            matrix[1][0], matrix[1][1], matrix[1][2], matrix[1][3],
            matrix[2][0], matrix[2][1], matrix[2][2], matrix[2][3],
            matrix[3][0], matrix[3][1], matrix[3][2], matrix[3][3]]

class BaseObject:
    def __init__(self):
        self._on_ready_callbacks: List[Callable[[Self], None]] = []
        self._on_update_callbacks: List[Callable[[Self], None]] = []
    
    def ready(self) -> None:
        for function in self._on_ready_callbacks:
            function(self)

    def update(self) -> None:
        for function in self._on_update_callbacks:
            function(self)
        self._object_update_method()

    def _object_update_method(self) -> None:
        pass

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
