
import json

from minefield import Minefield
import random
from solver import solver

# # 🟥 🟧 🟨 🟩 🟦 🟪 🟫 ⬛ ⬜


def ask_save(table, result, first_choice,  ask=False):
    # function to save the generated minefield, for easier future debugging
    saveble = []
    for row in table:
        new_row = []
        for tile in row:
            if tile.mine:
                new_row.append(-1)
            else:
                new_row.append(tile.mines_around)
        saveble.append(new_row)
    if ask:
        x = input("Would you like to save the generated table [y/N]?")
    else: 
        x = "y"
    try:
        if x != "":
            file_path = "saved.json"
            table_type = "solvable" if result else "unsolvable"
            with open(file_path, 'r') as file:
                data = json.load(file)
            if not isinstance(data, dict):
                data = {}
            if "solvable" not in data.keys():
                data["solvable"] = []
            if "unsolvable" not in data.keys():
                data["unsolvable"] = []
            data[table_type].extend([{"first_choice": first_choice, "table": saveble}])  

            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2,separators=(',', ': '))  # Write with indentation for readability

            # print("List extended successfully!")
    except:
        pass

def ask_load():
    # function for loading selected save if needed
    x = input("Which table would you like to upload?[<number>/N]")
    try:
        if x != "":
            # file_path = "mines/[py]_solve/to_load.json"
            file_path = "to_load.json"
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data["saved"][int(x)-1]
            
    except:
        pass

def fabric(forever=True):
    init_table = None
    init_table = ask_load()
    cont = True

    
    while cont:
        rows = 30
        columns = 30
        mines_percent = 10
        minefield = Minefield(rows,columns, mines_percent, init_table=init_table)

        # first choice should not be a mine, and the player shouldn't guess on the second turn
        first_choice = random.randint(0,rows-1),random.randint(0,columns-1)
        while minefield.table[first_choice[0]][first_choice[1]].mines_around != 0 or minefield.table[first_choice[0]][first_choice[1]].mine:
            first_choice = random.randint(0,rows-1),random.randint(0,columns-1)

        result = solver(minefield, first_choice)
        # print("SOLVED" if result else "UNSOLVABLE")
        ask_save(minefield.table,result, first_choice)
        # again = input("Again? [Y/n]\n")
        # cont = again == ""
        cont = forever


if __name__ == "__main__":
    fabric(True)
    


