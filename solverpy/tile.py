# # 🟥 🟧 🟨 🟩 🟦 🟪 🟫 ⬛ ⬜


class TileButton():
    def __init__(self, icolumn, irow, mine=False, mines_around=0):
        self.irow = irow
        self.icolumn = icolumn
        self.mine = mine
        self.mines_around = mines_around
        self.clicked = False
        self.flagged = False

        # self.selected = False
        self.highlighted = False
        self.highlighted_h = False
        self.highlighted_n = False

    def __eq__(self, other):
        return (self.irow == other.irow and 
        self.icolumn == other.icolumn and 
        self.clicked == other.clicked and 
        self.flagged == other.flagged and 
        self.mine == other.mine and 
        self.mines_around == other.mines_around)

    def __key(self):
        return (self.irow, self.icolumn)

    def __hash__(self):
        return hash(self.__key())


    def __gt__(self, other):
        return self.mines_around > self.mines_around

    def __repr__(self):
        if self.mine:
            return("🟥")
        else:
            return f" {self.mines_around}"
        
    def display(self, hidden=False):
        if hidden:
            if self.highlighted:
                return ("🟨")
            elif self.highlighted_n:
                return ("🟩")
            elif self.highlighted_h:
                return ("🟪")
            elif self.flagged:
                return ("⬛")
            elif not self.clicked:
                return ("⬜")
            else:
                if self.mine:
                    return("🟥")
                else:
                    return f" {self.mines_around}"
        else:
            if self.mine:
                return("🟥")
            else:
                return f" {self.mines_around}"
 
    def toggle_select(self):
        self.selected = not self.selected


    def reveal(self):
        if self.clicked:
            return
        self.clicked = True
        # self.color = self.active_color 
        if self.mine == True:
            return False
            # self.display = self.mine_image
        else:
            self.text = "" if self.mines_around == 0 else str(self.mines_around)
            return True
            # try:
            #     self.color = self.color_scheme[self.text]
            # except:
            #     self.color = self.color_scheme["0"]
            # self.display = self.font.render(self.text, True, (0, 0, 0))
            # else:
        #     self.clicked = False
            # self.color = self.default_color 



    def flag(self):
        if self.clicked:
            return 
        # if self.flagged:
        #     self.display = self.font.render(self.text, True, (0, 0, 0))
        # else:
        #     self.display = self.flag_image
        self.flagged = not self.flagged
        return True
            


    def inject_mine(self):
        self.mine = True
    
    def increment_mines_around(self):
        self.mines_around += 1