
import pygame
from pygame.locals import *
import random
import types

from clickableObject import ClickableObject, RED, WHITE



class Minefield():
    def __init__(self, rows, columns, minesize, margin, mines_percent):
        self.rows = rows
        self.columns = columns
        self.minesize = minesize
        self.margin = margin
        self.mines_count = rows*columns*mines_percent//100

        self.table = self.create_grid()
        self.distribute()
        self.hint_populate()

    def event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                pos = pygame.mouse.get_pos()
                for row in self.table:
                    for item in row:
                        if item.rect.collidepoint(pos):
                            if item.mines_around == 0:
                                self.clearfield(item.icolumn, item.irow)
                            else:
                                item.on_leftmouseclick()
            elif event.button == 3:  # Right mouse button clicked
                pos = pygame.mouse.get_pos()
                for row in self.table:
                    for item in row:
                        if item.rect.collidepoint(pos):
                            item.on_rightmouseclick()

    def clearfield(self, xstart, ystart):
        if self.table[ystart][xstart].clicked:
            return
        self.table[ystart][xstart].on_leftmouseclick()
        if self.table[ystart][xstart].mines_around != 0:
            return
        for tryout in [
            [ystart+1,xstart],
            [ystart,xstart+1],
            [ystart+1,xstart+1],
            [ystart-1,xstart],
            [ystart,xstart-1],
            [ystart-1,xstart-1],
            [ystart-1,xstart+1],
            [ystart+1,xstart-1],
            ]:
            try:
                if tryout[0] >=0 and tryout[1] >= 0 and tryout[0] < self.rows and tryout[1] < self.columns:
                
                    self.clearfield(tryout[1], tryout[0])
            except:
                pass

    def create_grid(self):
        table = []
        row_offset = 0
        for irow in range(self.rows):
            row = []
            columns_offset = 0
            for icol in range(self.columns):
                
                fill = TileButton( row_offset,
                                        columns_offset,
                                        icol,
                                        irow,
                                        self.minesize,
                                        self.minesize,
                                        (255, 255, 255),
                                        "")
                columns_offset += self.minesize + self.margin
                row.append(fill)

            row_offset += self.minesize + self.margin
            table.append(row)
        return table

        
    def distribute(self):
        rows = len(self.table)
        columns = len(self.table[0])

        mines_coordinates = []
        while self.mines_count >=0:
            mine_y_rows=random.randint(0, rows-1)
            mine_x_cols=random.randint(0, columns-1)
            if [mine_y_rows, mine_x_cols] in mines_coordinates:
                continue
            mines_coordinates.append([mine_y_rows, mine_x_cols])
            self.table[mine_y_rows][mine_x_cols].inject_mine()
            self.mines_count-=1

    def hint_populate(self):
        # populates the grid with numbered tiles corresponding to the number of surrounding mines
        rows = len(self.table)
        columns = len(self.table[0])
        for irow in range(len(self.table)):
            for icolumn in range(len(self.table[irow])):
                current = self.table[irow][icolumn]
                mines_around = 0
                for tryout in [
                        [irow+1,icolumn],
                        [irow,icolumn+1],
                        [irow+1,icolumn+1],
                        [irow-1,icolumn],
                        [irow,icolumn-1],
                        [irow-1,icolumn-1],
                        [irow-1,icolumn+1],
                        [irow+1,icolumn-1],
                        ]:
                    try:
                        if tryout[0] >=0 and tryout[1] >= 0 and tryout[0] < rows and tryout[1] < columns:
                            if self.table[tryout[0]][tryout[1]].mine == True:
                                current.increment_mines_around()
                    except:
                        pass



class TileButton(ClickableObject):
    def __init__(self, x, y, icolumn, irow, width, height, default_color, text):
        super().__init__(x, y, width, height, default_color, text)
        image_path = "extra/"
        mine_image_path = image_path+"mine.png"
        flag_image_path = image_path+"flag.png"
        self.mine_image = pygame.transform.scale(pygame.image.load(mine_image_path), (width, height))
        self.flag_image = pygame.transform.scale(pygame.image.load(flag_image_path), (width, height))
        self.irow = irow
        self.icolumn = icolumn
        
        self.clicked = False
        self.flagged = False
        self.mine = False
        self.mines_around = 0
        self.color_scheme = {
                            # "-1":
                            "0":(193, 191, 181),
                            "1":(67, 185, 41),
                            "2":(241, 196, 15),
                            "3":(255, 103, 0),
                            "4":(214, 40, 40),
                            "5":(214, 40, 40),
                            "6":(214, 40, 40),
                            "7":(214, 40, 40),
                            "8":(214, 40, 40),
                            
                                }
    
        

    def on_leftmouseclick(self):
        if self.clicked:
            return
        self.clicked = True
        self.color = self.active_color 
        if self.mine == True:
            self.display = self.mine_image
        else:
            self.text = "" if self.mines_around == 0 else str(self.mines_around)
            try:
                self.color = self.color_scheme[self.text]
            except:
                self.color = self.color_scheme["0"]
            self.display = self.font.render(self.text, True, (0, 0, 0))
            # else:
        #     self.clicked = False
            # self.color = self.default_color 

    def on_rightmouseclick(self):
        if self.clicked:
            return 
        if self.flagged:
            self.display = self.font.render(self.text, True, (0, 0, 0))
        else:
            self.display = self.flag_image
        self.flagged = not self.flagged
            


    def inject_mine(self):
        self.mine = True
    
    def increment_mines_around(self):
        self.mines_around += 1