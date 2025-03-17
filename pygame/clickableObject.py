import pygame
from pygame.locals import *
import random
import types

WHITE = (255, 255, 255)
RED = (255, 0, 0)


class ClickableObject():
    def __init__(self, x, y, width, height, default_color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.default_color = default_color
        self.font = pygame.font.Font(None, 36)
        self.display = self.font.render(text, True, (0, 0, 0))
        self.color = default_color
        self.active_color = RED
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_rect = self.display.get_rect(center=self.rect.center)
        
        screen.blit(self.display, text_rect)
    
    def on_leftmouseclick(self):
        pass