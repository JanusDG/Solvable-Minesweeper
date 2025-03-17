
import random
import types

from tile import TileButton


class Minefield():
    def __init__(self, rows, columns, mines_percent, init_table=None):
        self.rows = rows
        self.columns = columns
        self.mines_count = rows*columns*mines_percent//100

        if init_table is None:
            self.table = self.create_grid()
            self.distribute()
            self.hint_populate()
        else:
            self.table = self.create_from_init(init_table)
        # self.selected_coord=(None, None)

    def create_from_init(self, init_table):
        table = []
        for irow in range(self.rows):
            row = []
            for icol in range(self.columns):
                initial = init_table[irow][icol]
                if initial == -1:
                    # just in case there is a bug where we check for number of mines around a mine
                    # which shouln't happen
                    fill = TileButton(icol, irow, mine=True, mines_around=-100) 
                else:
                    fill = TileButton(icol, irow, mine=False, mines_around=initial) 
                row.append(fill)
            table.append(row)
        return table


    def click(self, row, col):
        # if not (self.selected_coord[0] is None):
        #     # deselect previous selected tile
        #     self.table[self.selected_coord[0]][self.selected_coord[1]].toggle_select()
        
        tile = self.table[row][col]
        # tile.toggle_select()

        if tile.mines_around == 0:
            return self.clearfield(tile.icolumn, tile.irow)
        else:
            return tile.reveal()
        # if tile.mine:
        #     return False
        # else:
        #     tile.reveal()
        #     return True
        
            

    def clearfield(self, xstart, ystart):
        if self.table[ystart][xstart].clicked:
            return
        x = self.table[ystart][xstart].reveal()
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
        return x

    def create_grid(self):
        table = []
        for irow in range(self.rows):
            row = []
            for icol in range(self.columns):
                fill = TileButton(icol, irow, )
                row.append(fill)
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

    def get_tile_neighbours(self,ystart, xstart):
        neighbors = []
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
                    neighbors.append(tryout)
            except:
                pass
        return neighbors
    
    def display(self):
        mrows = len(self.table)
        mcols = len(self.table[0])

        for irow in range(mrows):
            for icol in range(mcols):
                print(self.table[irow][icol].display(hidden=True), end="")
            print("|", end="")
            for icol in range(mcols):
                print(self.table[irow][icol], end="")
            print()
        print()


