import pygame
from pygame.locals import *
import random
import types

from clickableObject import ClickableObject, RED, WHITE


class MenuButton(ClickableObject):
    def __init__(self, x, y, width, height, default_color, text, on_left = (lambda:print(1)), on_right=(lambda:None)):
        super().__init__(x, y, width, height, default_color, text)
        self.on_left = on_left
        self.on_right = on_right
    def on_leftmouseclick(self):
        self.on_left()
    def on_rightmouseclick(self):
        self.on_right()

    

class Sidebar():
    def __init__(self, game):
        self.game = game
        def reset_on_leftmouseclick():
            game.reset_minefield()
        def exit_on_leftmouseclick():
            print("yes")
            exit(0)

        button_x_offset = 60 
        button_y_offset = 10
        button_width = 15 
        button_height = 40
        button_margin = 20 
        self.resetbutton = MenuButton(button_x_offset,
                                    button_y_offset,
                                    button_width,
                                    button_height,
                                    WHITE, "Reset", on_left=reset_on_leftmouseclick)
        self.exitbutton = MenuButton(button_x_offset,
                                    button_y_offset + button_height + button_margin,
                                    button_width,
                                    button_height,
                                    WHITE, "Exit", on_left=exit_on_leftmouseclick)

        self.buttons = [self.resetbutton, self.exitbutton]
    
    def event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(pos):
                        button.on_leftmouseclick()

            elif event.button == 3:  # Right mouse button clicked
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(pos):
                        button.on_rightmouseclick()
