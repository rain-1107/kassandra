import pygame


default_font = pygame.font.Font("freesansbold.ttf", 12)

def get_text_surf(text, font = default_font, colour = (0, 0, 0)):
    return font.render(text, False, colour)
    
