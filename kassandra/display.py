from types import FunctionType
from typing import List
from .utils import Vector2
import pygame
from .sprite import Sprite


class Display:
    def __init__(self, size: tuple[int, int] = (500, 500), fullscreen: bool = False, **kwargs):
        self.screen_surface: pygame.Surface
        if fullscreen:
            self.screen_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF)
        else:
            self.screen_surface = pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.delta_time: float = 1/60
        self.fps: int = kwargs.get("fps", 60)
        self._update_callback: FunctionType | None = kwargs.get("update_callback", None)
        self.running: bool = False
        self.cameras = []

    def set_update_callback(self, function: FunctionType) -> None:
        self._update_callback = function

    def update(self) -> None:
        for _ in pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            self.running = False
            return
        self.screen_surface.fill((100, 100, 100))
        if self._update_callback:
            self._update_callback(self.delta_time)
        for camera in self.cameras:
            camera.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.fps)

    def mainloop(self) -> None:
        self.running = True
        while self.running:
            self.update()

    def _add_camera(self, camera):
        self.cameras.append(camera)

class Camera:
    def __init__(self, display: Display, size: tuple[int, int] = (500, 500), position: tuple[int, int] = (0, 0), **kwargs):
        self.scale: float = kwargs.get("scale", 1)
        self._surface = pygame.Surface(size, pygame.SRCALPHA)
        self._display = display
        self._size = Vector2.list_to_vec(size)
        self._position = Vector2.list_to_vec(position)
        self.sprites: List[Sprite] = []

    def update(self):
        for sprite in self.sprites:
            sprite.draw(self._surface)
        self._display.screen_surface.blit(pygame.transform.scale(self._surface, [self._size.x * self.scale, self._size.y * self.scale]), self._position.list)
    
    def add_sprite(self, sprite: Sprite) -> None:
        if sprite not in self.sprites:
            self.sprites.append(sprite)

    def remove_sprite(self, sprite: Sprite) -> None:
        if sprite in self.sprites:
            self.sprites.remove(sprite)
