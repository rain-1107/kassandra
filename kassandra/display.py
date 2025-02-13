from types import FunctionType
import pygame


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

    def set_update_callback(self, function: FunctionType) -> None:
        self._update_callback = function

    def update(self) -> None:
        for _ in pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            self.running = False
            return
        if self._update_callback:
            self._update_callback(self.delta_time)
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.fps)

    def mainloop(self) -> None:
        self.running = True
        while self.running:
            self.update()
