import random
import pygame
from .gui import get_text_surf


def read_file(filename: str):
    file = open(filename, "r")
    text = file.read()
    file.close()
    return text


_image_cache = {}


def load_image(image_file: str, size = (50, 50)) -> pygame.Surface:
    if type(image_file) == str:
        if image_file in _image_cache:
            return _image_cache[image_file]
        try:
            _image = pygame.image.load(image_file).convert_alpha()
            _image = pygame.transform.scale(_image, size)
            _image_cache[image_file] = _image
        except FileNotFoundError:
            _surf = pygame.surface.Surface(size)
            _surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            text = get_text_surf(f"{image_file}")
            _surf.blit(text,
                       ((size[0] / 2) - (text.get_size()[0] / 2), (size[1] / 2) - (text.get_size()[1] / 2)))
            _image = _surf.convert()
        return _image
    raise TypeError("Image file is not a string")

