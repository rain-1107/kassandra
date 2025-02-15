import math
from typing import List

class Vector2:
    @staticmethod
    def list_to_vec(lst):
        if type(lst) == tuple or type(lst) == list:
            return Vector2(*lst)
        return lst

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def unit(self):
        dist: float = self.magnitude() 
        self.x = self.x/dist
        self.y = self.y/dist

    def magnitude(self):
        return math.sqrt(self.x**2+self.y**2) 

    def set(self, other):
        self.x = other.x
        self.y = other.y

    def __add__(self, other):
        return Vector2(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vector2(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x*other.x, self.y*other.y)
        return Vector2(self.x*other, self.y*other)
    
    def __rmul__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x*other.x, self.y*other.y)
        return Vector2(self.x*other, self.y*other)

    def __truediv__(self, other):
        return Vector2(self.x/other.x, self.y/other.y)

    def __str__(self):
        return "x: {x}, y: {y}".format(x=self.x, y=self.y)

    def snap_to_grid(self, grid_size_x, grid_size_y, apply=False):
        snapped_x = round(self.x / grid_size_x) * grid_size_x
        snapped_y = round(self.y / grid_size_y) * grid_size_y
        if apply:
            self.x = snapped_x
            self.y = snapped_y
        return snapped_x, snapped_y

    def copy(self):
        return Vector2(self.x, self.y)

    @property
    def list(self) -> List[float]:
        return [self.x, self.y]

    @property
    def tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

