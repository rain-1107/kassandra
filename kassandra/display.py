import os
import sys
import pygame
import numpy


class Display:
    def __init__(self, size: tuple[int, int] = (500, 500), fullscreen: bool = False, **kwargs):
        self.surface: pygame.Surface
        if fullscreen:
            self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF)
        else:
            self.surface = pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.delta_time: float = 1/60
        self.fps: int = kwargs.get("fps", 60)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        self.clock.tick(self.fps)