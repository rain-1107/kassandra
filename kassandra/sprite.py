from typing import Tuple, Optional
import pygame
from .math_utils import Vector2
from .load import load_image
from .base import Base
from copy import deepcopy

class Sprite(Base):
    def __init__(self, size: Tuple[int, int] | Vector2, position: Tuple[int, int] | Vector2, image: Optional[pygame.Surface] = None, **kwargs):
        super().__init__()
        self.size: Vector2 = Vector2.list_to_vec(size) 
        self._image = image
        self.centered = kwargs.get("centered", False)
        self.id = kwargs.get("id", 0)
        self.tag = kwargs.get("tag", "")
        self._top_left: Vector2 = Vector2(0, 0)
        self._centre: Vector2 = Vector2(0, 0)
        self.position = Vector2.list_to_vec(position) 
        self.delta_time: float = 1/60

    def update(self, surf: pygame.Surface, dt: float = 1/60, position_offset: Vector2 | None = None):
        self.delta_time = dt
        if self._update_callback:
            self._update_callback(self)
        if position_offset:
            surf.blit(self.image, (self._top_left + position_offset).list)
            return
        surf.blit(self.image, self._top_left.list)
    
    @property
    def image(self) -> pygame.Surface:
        if self._image:
            return self._image
        raise TypeError("Image is None")

    @property
    def position(self) -> Vector2:
        if self.centered:
            return self._centre
        return self.top_left

    @position.setter
    def position(self, new: Vector2):
        if self.centered:
            self._centre = new.copy()
            return
        self.top_left = new.copy()


class AnimatedSprite(Sprite):
    def __init__(self, size, position, image_data: dict, **kwargs):
        super().__init__(size, position, **kwargs)
        self.raw_data = deepcopy(image_data)
        self.image_data = deepcopy(image_data)
        for list in self.image_data:
            temp = []
            for image in self.image_data[list]["images"]:
                image = load_image(image, self.size.list)
                temp.append(image)
            self.image_data[list]["images"] = temp
        self.index = 0
        self.tick = 0
        self.state = next(iter(self.image_data))
        self.previous_state = next(iter(self.image_data))

    def update(self, surf: pygame.Surface, dt: float = 1/60, position_offset: Vector2 | None = None):
        self.delta_time = dt
        if self._update_callback:
            self._update_callback(self)
        self.tick -= self.delta_time
        if self.tick < 0:
            self.tick = self.image_data[self.state]["tick"]
            self.index += 1
            if self.index > self.image_data[self.state]["images"].__len__() - 1:
                if self.image_data[self.state]["loop"]:
                    self.index = 0
                else:
                    self.change_state(self.previous_state)
            self._image = self.image_data[self.state]["images"][self.index]
        if position_offset:
            surf.blit(self.image, (self._top_left + position_offset).list)
            return
        surf.blit(self.image, self._top_left.list)

    def change_state(self, new_state):
        self.previous_state = self.state
        self.state = new_state
        self.index = -1
        self.tick = 0
