import pygame
from pygame.locals import *
import random
import types
import sys

from clickableObject import ClickableObject, RED, WHITE
from minefield import Minefield
from sidebar import Sidebar
# # 🟥 🟧 🟨 🟩 🟦 🟪 🟫 ⬛ ⬜




class Gamedisplay():
    def __init__(self, resolution):
        pygame.init()
        self.screen = pygame.display.set_mode((resolution[0], resolution[1]))
        pygame.display.set_caption('Mines game')
        self.resolution = resolution

        self.rows=10
        self.columns=10
        self.minefield = Minefield(rows = self.rows,
                        columns = self.columns,
                        minesize = 50,
                        margin = 5,
                        mines_percent = 10)
        self.sidebar = Sidebar(self) 

    def reset_minefield(self):
        self.minefield = Minefield(rows = self.rows,
                        columns = self.columns,
                        minesize = 50,
                        margin = 5,
                        mines_percent = 10)

    def event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                self.sidebar.event(event)
                self.minefield.event(event)
            
    def draw(self):
        self.screen.fill((0, 0, 0))
        for row in self.minefield.table:
            for item in row:
                # print(item.text)
                item.draw(self.screen)
        for button in self.sidebar.buttons:
            button.draw(self.screen)
    def launch(self):
        while True:
            self.event()
            self.draw()
            pygame.display.flip()


if __name__ == "__main__":
    resolution = (800, 600)
    
    gamedisplay = Gamedisplay(resolution)
    gamedisplay.launch()



