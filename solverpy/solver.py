import random
import types
import sys
import time
from itertools import product, combinations
from constraint import *

def check_if_solved(minefield):
    # checks if the given minefield is solved or not    
    for row in minefield.table:
        for item in row:
            # if the tile doesn't contain a mine and it's not clicked, the game isn't finished
            if (not item.mine) and (not item.clicked):
                return False
    return True

def solver(minefield, first_choice):
    # algorithms to solve the minesweeper's field of mines    
    minefield.click(first_choice[0],first_choice[1])

    mrows = len(minefield.table)
    mcols = len(minefield.table[0])

    # dummy logic for prioritizing the rule checks
    # TODO rewrite this dumbassary
    global_point = True
    def easy_moves(minefield):

        point = True
        # continue to try easy moves, if in previous iteration had a successful easy move
        while point:
            point = False
            for irow in range(mrows):
                for icol in range(mcols):
                    tile = minefield.table[irow][icol]
                    
                    # skip, until you find a reveled numbered tile
                    if not tile.clicked or tile.mines_around == 0:
                        continue
                    
                    # check if you can make an easy move
                    if check_rule1(minefield,irow,icol):
                        # time.sleep(0.01)
                        # minefield.display()
                        point = True
                        global_point = True
                    if check_rule2(minefield,irow,icol):
                        # time.sleep(0.01) 
                        # minefield.display()
                        point = True
                        global_point = True

    while global_point:
        global_point = False
        easy_moves(minefield)
        # ask_save(minefield.table,ask=True)

        if create_constraint(minefield):
            minefield.display()
            global_point=True
        

        if check_if_solved(minefield):
            return True

    return False



def check_rule1(minefield, y,x):
    # checks if number of hidden tiles around a tile = tier of a tile
    # if so, all hidden neighboring tiles are bombs
    neighbours = [minefield.table[n_y][n_x] for n_y,n_x in minefield.get_tile_neighbours(y,x)]
    if minefield.table[y][x].mines_around == sum(1 for x in neighbours if (not x.clicked and not x.flagged))+sum(1 for x in neighbours if x.flagged):
        for x in neighbours:
            if not x.clicked and not x.flagged:
                return x.flag()
    return False

def check_rule2(minefield, y,x):
    # checks if number of flagged tiles around a tile = tier of a tile
    # if so, all hidden neighboring tiles are save
    neighbours = [minefield.table[n_y][n_x] for n_y,n_x in minefield.get_tile_neighbours(y,x)]
    if minefield.table[y][x].mines_around == sum(1 for x in neighbours if x.flagged):
        for x in neighbours:
            if not x.clicked and not x.flagged:
                return minefield.click(x.irow, x.icolumn)#x.reveal()
    return False



def create_constraint(minefield):
    hidden_chain = []
    numbered_chain = []
    def find_chain_of_hidden(chain, tile):
        # finds an outer layer of the hidden tiles, which could not be solved with easy moves
        # TODO: check if it's really only outer layer or not
        neighbours = [minefield.table[n_y][n_x] for n_y,n_x in minefield.get_tile_neighbours(tile.irow,tile.icolumn)]
        hidden_neighbours = list(filter(lambda tile: not tile.flagged and not tile.clicked, neighbours))
        numbered_neighbours = list(filter(lambda tile: tile.clicked and tile.mines_around > 0, neighbours))
        
        # recurcion exit, if there are no hidden neighbors, or all of the hidden neighbours are already in the chain
        if len(hidden_neighbours) == 0 or len(numbered_neighbours)== 0:
            return
        
        # if all hidden neighbours are in chain:
        chain.append(tile)
        ret = True
        for item in hidden_neighbours:
            if item not in chain:
                ret = False
                break
        if ret:
            return

        # chain.extend([neighbour for neighbour in hidden_neighbours if neighbour not in chain])
        # recurcion call, find the hidden neighbours of all numbered heighbours of a tile
        for nn in hidden_neighbours:
            if nn not in chain:
                find_chain_of_hidden(chain, nn)
    
    def find_chain_of_numbered_with_hidden(chain, tile):
        # finds an outer layer of the numbered tiles, around the hidden tiles
        neighbours = [minefield.table[n_y][n_x] for n_y,n_x in minefield.get_tile_neighbours(tile.irow,tile.icolumn)]
        hidden_neighbours = list(filter(lambda tile: not tile.flagged and not tile.clicked, neighbours))
        numbered_neighbours = list(filter(lambda tile: tile.clicked and tile.mines_around > 0, neighbours))
        numbered_neighbours_with_hidden_neighbours = list(filter(lambda x: list(filter(lambda tile: not tile.flagged and not tile.clicked, [minefield.table[n_y][n_x] for n_y,n_x in minefield.get_tile_neighbours(x.irow,x.icolumn)])) != []
                                                                 , numbered_neighbours))
        
        if len(numbered_neighbours_with_hidden_neighbours) == 0:
            return
        ret = True
        for item in numbered_neighbours_with_hidden_neighbours:
            if item not in chain:
                ret = False
        if ret:
            return
        chain.extend([neighbour for neighbour in numbered_neighbours_with_hidden_neighbours if neighbour not in chain])
        

        for nn in numbered_neighbours_with_hidden_neighbours:
            find_chain_of_numbered_with_hidden(chain, nn)
    
    def find_both_chains_by_numbered(chains, tile, daddy_tile):
        # finds chains of adjecent hidden and numbered tiles
        # Flaw in approach:
            # Because the search is going through the numbered tiles, if the
            # chain is interrupted by the flagged tile, the chains are considered
            # separate, and in the below case don't have one solution this way,
            # but chains 2 and 3 have unique solution if considered as one chain
            # ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
            # 1 2 ⬛ 2 2 2⬛ 2 1 1
        # Possible work around: combine some small chains to achieve solution
        # The only question is is it better than considering them as one, and then dividing
        # Another work around: consider chains by hidden tiles
        
        # recursion for finding pair of chains, one consisting of numbered tiles, another of hidden
        # each tile belonging to chain of numbered tiles has at least one neighboring hidden tile in hidden chain
        # and vise versa. The finding process is done by going through the numbered tiles 
        daddy_tile_id = f"{daddy_tile.irow}x{daddy_tile.icolumn}"

        if daddy_tile_id not in chains.keys():
            chains[daddy_tile_id] = {
                "numbered":[],
                "hidden":[],
            }

        # skip if a tile isn't non-zero numbered tile
        if not tile.clicked or tile.mines_around == 0:
            return
        # finds an outer layer of the numbered tiles, around the hidden tiles
        neighbours = [minefield.table[n_y][n_x] for n_y,n_x in minefield.get_tile_neighbours(tile.irow,tile.icolumn)]
        hidden_neighbours = list(filter(lambda tile: not tile.flagged and not tile.clicked, neighbours))
        numbered_neighbours = list(filter(lambda tile: tile.clicked and tile.mines_around > 0, neighbours))
        numbered_neighbours_with_hidden_neighbours = list(filter(lambda x: list(filter(lambda tile: not tile.flagged and not tile.clicked, [minefield.table[n_y][n_x] for n_y,n_x in minefield.get_tile_neighbours(x.irow,x.icolumn)])) != []
                                                                 , numbered_neighbours))# так, сам додумався
        
        # recurcion exit, if there are no hidden neighbors, or all of the hidden neighbours are already in the chain
        if len(hidden_neighbours) == 0 or len(numbered_neighbours)== 0:
            return
        if len(numbered_neighbours_with_hidden_neighbours) == 0:
            return
        if tile in chains[daddy_tile_id]["numbered"]:
            return
        
        chains[daddy_tile_id]["numbered"].append(tile)
        chains[daddy_tile_id]["hidden"].extend([neighbour for neighbour in hidden_neighbours if neighbour not in chains[daddy_tile_id]["hidden"]])
        ret = True
        # if all numbered neighbours with hidden neighbours are in chain:
        ret = True
        for item in numbered_neighbours_with_hidden_neighbours:
            if item not in chains[daddy_tile_id]["numbered"]:
                ret = False
        if ret:
            return

        for nn in numbered_neighbours_with_hidden_neighbours:
            find_both_chains_by_numbered(chains, nn, daddy_tile)

    def find_both_chains_by_hidden(chains, tile, daddy_tile):
        # skip if the tile is not hidden
        if tile.clicked:
            return

        daddy_tile_id = f"{daddy_tile.irow}x{daddy_tile.icolumn}"
        if daddy_tile_id not in chains.keys():
            chains[daddy_tile_id] = {
                "numbered":[],
                "hidden":[],
                "flagged":[],
            }

        # finds an outer layer of the numbered tiles, around the hidden tiles
        neighbours = [minefield.table[n_y][n_x] for n_y,n_x in minefield.get_tile_neighbours(tile.irow,tile.icolumn)]
        hidden_neighbours = list(filter(lambda tile: not tile.flagged and not tile.clicked, neighbours))

        # flagged neighbours also should be included in the equasion, as they are the part of number inside numbered tile
        flagged_neighbours = list(filter(lambda tile: tile.flagged, neighbours))
        numbered_neighbours = list(filter(lambda tile: tile.clicked and tile.mines_around > 0, neighbours))
        numbered_neighbours_with_hidden_neighbours = list(filter(lambda x: list(filter(lambda tile: not tile.flagged and not tile.clicked, [minefield.table[n_y][n_x] for n_y,n_x in minefield.get_tile_neighbours(x.irow,x.icolumn)])) != []
                                                                 , numbered_neighbours))# так, сам додумався
        hidden_or_flagged_neighbours_with_numbered_neighbours = list(filter(lambda x: 
                                                         list(filter(lambda tile: tile.clicked and tile.mines_around != 0,
                                                         [minefield.table[n_y][n_x] for n_y,n_x in minefield.get_tile_neighbours(x.irow,x.icolumn)])) != [],
                                                     hidden_neighbours+flagged_neighbours))# так, сам додумався                                                         
        
        # recurcion exit, if there are no hidden neighbors, or all of the hidden neighbours are already in the chain
        if len(hidden_neighbours) == 0 or len(numbered_neighbours)== 0:
            return
        if len(hidden_or_flagged_neighbours_with_numbered_neighbours) == 0:
            return
        if tile in chains[daddy_tile_id]["hidden"]:
            return
        
        if tile in chains[daddy_tile_id]["flagged"]:
            return
        
        # remove later
        # if f"{daddy_tile.irow}x{daddy_tile.icolumn}" == "0x0

        # do not add flagged tiles to the chain
        if not tile.flagged:
            chains[daddy_tile_id]["hidden"].append(tile)
        else:
            chains[daddy_tile_id]["flagged"].append(tile)
        chains[daddy_tile_id]["numbered"].extend([neighbour for neighbour in numbered_neighbours if neighbour not in chains[daddy_tile_id]["numbered"]])
        ret = True
        # if all hidden neighbours with numbered neighbours are in chain:
        ret = True
        for item in hidden_or_flagged_neighbours_with_numbered_neighbours:
            if item not in chains[daddy_tile_id]["hidden"]:
                ret = False
        if ret:
            return
        
        
        for nn in hidden_or_flagged_neighbours_with_numbered_neighbours:
            find_both_chains_by_hidden(chains, nn, daddy_tile)
    
    # each hidden tile in the chain is a variable
    
    # point = True
    # # retry if there is at least one deterministically solvable chain
    # while point:
    # new chains for each retry
    chains = {}
    # point = False

    mrows = len(minefield.table)
    mcols = len(minefield.table[0])

    # find chains of hidden 
    for irow in range(mrows):
        for icol in range(mcols):
            tile = minefield.table[irow][icol]
            daddy_tile_id = f"{tile.irow}x{tile.icolumn}"
            find_both_chains_by_hidden(chains,tile, tile)

            # if the chain is found, and it's non-empty
            if daddy_tile_id in chains.keys() and len(chains[daddy_tile_id]["numbered"])  != 0 and len(chains[daddy_tile_id]["hidden"])  != 0:
                # if the same chain already exist in another tile, remove the chain
                # TODO consider not adding it in the first place
                if  any(
                    all(set(chains[daddy_tile_id][key]) == set(chains[k][key]) for key in chains[daddy_tile_id])
                    for k in chains if k != daddy_tile_id
                    ):
                    chains.pop(daddy_tile_id, None)
                    continue
                
                # minefield.display  chains 
                for item in chains[daddy_tile_id]["numbered"]:
                    item.highlighted_n = True
                for item in chains[daddy_tile_id]["hidden"]:
                    item.highlighted_h = True
                
                minefield.display()
                for item in chains[daddy_tile_id]["numbered"]:
                    item.highlighted_n = False
                for item in chains[daddy_tile_id]["hidden"]:
                    item.highlighted_h = False
            else:
                # if the chain is empty, remove it 
                chains.pop(daddy_tile_id, None)


    # # create a constraint for each chain
    for tile_id, value in chains.items():
        hidden_chain = value["hidden"]
        numbered_chain = value["numbered"]
        # constraint creator
        problem = Problem()
        # each numbered tile of the chain is used to create a constraint
        for tile in numbered_chain:
            neighbours = [minefield.table[n_y][n_x] for n_y,n_x in minefield.get_tile_neighbours(tile.irow,tile.icolumn)]
            hidden_neighbours = list(filter(lambda tile: not tile.flagged and not tile.clicked, neighbours))
            flagged_neighbours = sum(1 for x in neighbours if x.flagged)
            summ = tile.mines_around - flagged_neighbours

            for tile in hidden_neighbours:
                try:
                    problem.addVariable(f"{tile.irow}x{tile.icolumn}",[0,1])
                except ValueError:
                    continue

            # don't ask
            walrus = list(set([f"{tile.irow}x{tile.icolumn}" for tile in hidden_neighbours]))
            # happends when the numbered tile in the chain has only flagged and numbered neighbours 
            if len(walrus) == 0:
                continue


            problem.addConstraint(ExactSumConstraint(summ), walrus)
        
        solutions = problem.getSolutions()
            
        # we care only if the chain could be solved deterministically
        # TODO: consider partly solved constraint if all of the solutions have the same 
        # values for some subset of variables
        #
        # MAYBE: consider the solution before adding each constraint 
        #       NO, because we don't consider the other end of iteration of a chain, 
        #           which appears while itteratively creating the constrains
        if len(solutions) == 0:
            continue
        
        if len(solutions) == 1:
            # reveal/flag the tiles according to the solution
            for cords, value in solutions[0].items():
                irow = int(cords[0])
                icolumn = int(cords[-1])
                if value == 1:
                    minefield.table[irow][icolumn].flagged = True
                if value == 0:
                    minefield.click(irow, icolumn)
                time.sleep(0.01)
                minefield.display()
        else:
            # if there are more than 1 solution, find the partial solution, that appears in all of them
            common = {k: v for k, v in solutions[0].items() if all(d[k] == v for d in solutions)}
            if common == {}:
                continue
            for cords, value in common.items():
                irow = int(cords[:cords.index("x")])
                icolumn = int(cords[cords.index("x")+1:])
                if value == 1:

                    minefield.table[irow][icolumn].flagged = True

                if value == 0:

                    minefield.click(irow, icolumn)

                
                time.sleep(0.01)
                minefield.display()  
                

                # exit(0)
    return False


