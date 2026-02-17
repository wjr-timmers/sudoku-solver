import time
import itertools
from collections import defaultdict

VALUES = [1,2,3,4,5,6,7,8,9]

def print_grid(grid):
    for row in grid:
        print(f"{row}")
    return


def check_block(grid, temp_options, cell_coordinate, verbose=False):

    row_idx,col_idx = cell_coordinate
    # Top left block
    if (row_idx <3) and (col_idx <3):
        coordinates = ((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2))
        coordinates = [(i,j) for i in range(0,3) for j in range(0,3)]

    # Top middle block
    if (row_idx<3) and (3<= col_idx <6):
        coordinates = [(i,j) for i in range(0,3) for j in range(3,6)]

    # Top right block
    if (row_idx<3) and (col_idx >=6):
        coordinates = [(i,j) for i in range(0,3) for j in range(6,9)]

    # Middle left block
    if (3 <= row_idx <6) and (col_idx <3):
        coordinates = [(i,j) for i in range(3,6) for j in range(0,3)]

    # Middle middle block
    if (3 <= row_idx <6) and (3<= col_idx <6):
        coordinates = ((3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5))
        coordinates = [(i,j) for i in range(3,6) for j in range(3,6)]

    # Middle right block
    if (3 <= row_idx <6) and (col_idx >=6):
        coordinates = [(i,j) for i in range(3,6) for j in range(6,9)]

    # Bottom left block
    if (row_idx >= 6) and (col_idx <3):
        coordinates = [(i,j) for i in range(6,9) for j in range(0,3)]

    # Bottom middle block
    if (row_idx >= 6) and (3<= col_idx <6):
        coordinates = [(i,j) for i in range(6,9) for j in range(3,6)]

    # Bottom right block
    if (row_idx >= 6) and (col_idx >=6):
        coordinates = ((6,6),(6,7),(6,8),(7,6),(7,7),(7,8),(8,6),(8,7),(8,8))
        coordinates = [(i,j) for i in range(6,9) for j in range(6,9)]
    
    coordinates.remove((row_idx,col_idx))

    for i,j in coordinates:
        value = grid[i][j]
        if value in temp_options:
            temp_options.remove(value)
    
    return temp_options


def check_hidden(list_of_possibilities_in_block, flag="None", verbose=False, hidden_quant=2):
    
    occurences = {}
    for v in VALUES:
        occurences[v] = {
        'count': 0, 
        'coordinates': []
    }

    #print(list_of_possibilities_in_block)
    for coordinate, values in list_of_possibilities_in_block:
        if values == [0]:
            continue
        else:
            for value in values:
                occurences[value]['count'] += 1
                occurences[value]['coordinates'].append(coordinate)

    coord_groups = defaultdict(list)

    for num, data in occurences.items():
        if data['count'] == hidden_quant:
            coord_key = tuple(data['coordinates'])
            coord_groups[coord_key].append(num)

    for coords, numbers_hidden in coord_groups.items():
        if len(numbers_hidden) == hidden_quant:
            #print(f"|------------- Hidden Quant Found! Numbers {numbers_hidden} at {coords}")

            coords = list(coords)

            for coordinate, values in list_of_possibilities_in_block:
                if coordinate in coords:
                    for v in values[:]:
                        if v in numbers_hidden:
                            continue
                        else:
                            if verbose:
                                type_name = {1: "single", 2: "pair", 3: "triple", 4: "quad"}.get(hidden_quant, "set")
                                print(f"|-0--0--0-- Removed {v} from cell {coordinate} (hidden {type_name}, {flag})")
                            values.remove(v)


    return list_of_possibilities_in_block

def check_naked_single(list_of_possibilities_in_block, flag="None",verbose=False):
    
    naked_singles= []
    singles = [x for x in list_of_possibilities_in_block if (len(x[1])==1)]

    for (idx1, val1) in singles:
        single_values = [val1]
        single_indices = [idx1]
        union = set().union(*single_values)

        if len(union) == 1:
            naked_singles.append((idx1,val1))

    if len(naked_singles) != 0:
        naked_pair_coordinates = set(coord for coord, vals in naked_singles)

        for coordinate, values in list_of_possibilities_in_block:
            # Skip if this cell IS part of the naked single
            if coordinate in naked_pair_coordinates:
                continue
            
            # Remove naked single values from other cells
            for naked_coord, naked_values in naked_singles:
                for naked_value in naked_values:
                    if naked_value in values[:]:
                        if verbose:
                            print(f"|---------- Removed {naked_value} from {values} in cell {coordinate} (naked single, {flag})")
                        values.remove(naked_value)

    return list_of_possibilities_in_block

def check_naked_pairs(list_of_possibilities_in_block, flag="None",verbose=False):
    
    naked_pairs= []
    pairs = [x for x in list_of_possibilities_in_block if (len(x[1])==2)]

    for (idx1, val1), (idx2, val2) in itertools.combinations(pairs,2):
        pair_values = [val1] + [val2]
        pair_indices = [idx1] + [idx2]
        union = set().union(*pair_values)

        if len(union) == 2:
            naked_pairs.append((idx1,val1))
            naked_pairs.append((idx2,val2))

    if len(naked_pairs) != 0:
        naked_pair_coordinates = set(coord for coord, vals in naked_pairs)

        for coordinate, values in list_of_possibilities_in_block:
            # Skip if this cell IS part of the naked pair
            if coordinate in naked_pair_coordinates:
                continue
            
            # Remove naked pair values from other cells
            for naked_coord, naked_values in naked_pairs:
                for naked_value in naked_values:
                    if naked_value in values[:]:
                        if verbose:
                            print(f"|---------- Removed {naked_value} from {values} in cell {coordinate} (naked pair, {flag})")
                        values.remove(naked_value)

    return list_of_possibilities_in_block


def check_naked_triples(list_of_possibilities_in_block, flag="None",verbose=False):
    
    naked_triples = []
    triples_and_pairs = [x for x in list_of_possibilities_in_block if (len(x[1])==2 or len(x[1])==3)]

    for (idx1, val1), (idx2, val2), (idx3, val3) in itertools.combinations(triples_and_pairs,3):
        triple_values = [val1] + [val2] + [val3]
        triple_indices = [idx1] + [idx2] + [idx3]
        union = set().union(*triple_values)

        if len(union) == 3:
            naked_triples.append((idx1,val1))
            naked_triples.append((idx2,val2))
            naked_triples.append((idx3,val3))

    if len(naked_triples) != 0:
        naked_triple_coordinates = set(coord for coord, vals in naked_triples)

        for coordinate, values in list_of_possibilities_in_block:
            # Skip if this cell IS part of the naked triple
            if coordinate in naked_triple_coordinates:
                continue
            
            # Remove naked triple values from other cells
            for naked_coord, naked_values in naked_triples:
                for naked_value in naked_values:
                    if naked_value in values[:]:
                        if verbose:
                            print(f"|---------- Removed {naked_value} from {values} in cell {coordinate} (naked triple, {flag})")
                        values.remove(naked_value)

    return list_of_possibilities_in_block


def check_naked_quads(list_of_possibilities_in_block, flag="None",verbose=False):
    
    naked_quads = []
    quads_triples_and_pairs = [x for x in list_of_possibilities_in_block if (len(x[1])==2 or len(x[1])==3 or len(x[1])==4)]

    for (idx1, val1), (idx2, val2), (idx3, val3), (idx4, val4) in itertools.combinations(quads_triples_and_pairs,4):
        quad_values = [val1] + [val2] + [val3] + [val4]
        quad_indices = [idx1] + [idx2] + [idx3] + [idx4]
        union = set().union(*quad_values)

        if len(union) == 4:
            naked_quads.append((idx1,val1))
            naked_quads.append((idx2,val2))
            naked_quads.append((idx3,val3))
            naked_quads.append((idx4,val4))

    if len(naked_quads) != 0:
        naked_quad_coordinates = set(coord for coord, vals in naked_quads)

        for coordinate, values in list_of_possibilities_in_block:
            # Skip if this cell IS part of the naked quad
            if coordinate in naked_quad_coordinates:
                continue
            
            # Remove naked quad values from other cells
            for naked_coord, naked_values in naked_quads:
                for naked_value in naked_values:
                    if naked_value in values[:]:
                        if verbose:
                            print(f"|---------- Removed {naked_value} from {values} in cell {coordinate} (naked quad, {flag})")
                        values.remove(naked_value)

    return list_of_possibilities_in_block


def check_block_options(option_grid, cell_coordinate, verbose=False):

    row_idx,col_idx = cell_coordinate
    current_possibilities = option_grid[row_idx][col_idx]

    # Top left block
    if (row_idx <3) and (col_idx <3):
        coordinates_block = [(i,j) for i in range(0,3) for j in range(0,3)]

    # Top middle block
    if (row_idx<3) and (3<= col_idx <6):
        coordinates_block = [(i,j) for i in range(0,3) for j in range(3,6)]

    # Top right block
    if (row_idx<3) and (col_idx >=6):
        coordinates_block = [(i,j) for i in range(0,3) for j in range(6,9)]

    # Middle left block
    if (3 <= row_idx <6) and (col_idx <3):
        coordinates_block = [(i,j) for i in range(3,6) for j in range(0,3)]

    # Middle middle block
    if (3 <= row_idx <6) and (3<= col_idx <6):
        coordinates_block = [(i,j) for i in range(3,6) for j in range(3,6)]

    # Middle right block
    if (3 <= row_idx <6) and (col_idx >=6):
        coordinates_block = [(i,j) for i in range(3,6) for j in range(6,9)]

    # Bottom left block
    if (row_idx >= 6) and (col_idx <3):
        coordinates_block = [(i,j) for i in range(6,9) for j in range(0,3)]

    # Bottom middle block
    if (row_idx >= 6) and (3<= col_idx <6):
        coordinates_block = [(i,j) for i in range(6,9) for j in range(3,6)]

    # Bottom right block
    if (row_idx >= 6) and (col_idx >=6):
        coordinates_block = [(i,j) for i in range(6,9) for j in range(6,9)]
    
    coordinates_col = [(i, col_idx) for i in range(0,9)]
    coordinates_row = [(row_idx,j) for j in range(0,9)]

    list_of_possibilities_block_total = []
    list_of_possibitlies_row_total = []
    list_of_possibitlies_col_total = []

    for i,j in coordinates_block:
        list_of_possibilities_block_total.append(((i,j),option_grid[i][j])) # Cell coordinates and possible values
    
    for i,j in coordinates_row:
        list_of_possibitlies_row_total.append(((i,j), option_grid[i][j]))

    for i,j in coordinates_col:
        list_of_possibitlies_col_total.append(((i,j), option_grid[i][j]))


    assert len(list_of_possibilities_block_total) == 9
    assert len(list_of_possibitlies_row_total) == 9
    assert len(list_of_possibitlies_col_total) == 9

    list_of_possibilities_block_total = check_naked_single(list_of_possibilities_block_total, flag='block',verbose=verbose)
    list_of_possibitlies_row_total = check_naked_single(list_of_possibitlies_row_total, flag='row',verbose=verbose)
    list_of_possibitlies_col_total= check_naked_single(list_of_possibitlies_col_total, flag='col',verbose=verbose)

    list_of_possibilities_block_total = check_naked_pairs(list_of_possibilities_block_total, flag='block',verbose=verbose)
    list_of_possibitlies_row_total = check_naked_pairs(list_of_possibitlies_row_total, flag='row',verbose=verbose)
    list_of_possibitlies_col_total= check_naked_pairs(list_of_possibitlies_col_total, flag='col',verbose=verbose)

    list_of_possibilities_block_total = check_naked_triples(list_of_possibilities_block_total, flag="block",verbose=verbose)
    list_of_possibitlies_row_total = check_naked_triples(list_of_possibitlies_col_total, flag="row",verbose=verbose)
    list_of_possibitlies_col_total = check_naked_triples(list_of_possibitlies_row_total, flag="col",verbose=verbose)

    list_of_possibilities_block_total = check_naked_quads(list_of_possibilities_block_total, flag="block",verbose=verbose)
    list_of_possibitlies_row_total = check_naked_quads(list_of_possibitlies_col_total, flag="row",verbose=verbose)
    list_of_possibitlies_col_total = check_naked_quads(list_of_possibitlies_row_total, flag="col",verbose=verbose)

    # Check the hidden single, pairs, triples and quads
    for i in range(1,5):
        list_of_possibilities_block_total = check_hidden(list_of_possibilities_block_total, flag="block",verbose=verbose, hidden_quant=i)
        list_of_possibitlies_row_total = check_hidden(list_of_possibitlies_col_total, flag="row",verbose=verbose, hidden_quant=i)
        list_of_possibitlies_col_total = check_hidden(list_of_possibitlies_row_total, flag="col",verbose=verbose, hidden_quant=i)

    list_of_possibilities = list_of_possibilities_block_total + list_of_possibitlies_row_total + list_of_possibitlies_col_total
    list_of_possibilities = [item for item in list_of_possibilities if item[0] != cell_coordinate]


    # Deduplicate by coordinate - keep the LONGEST valid list (not [0] or empty)
    coord_dict = {}
    for coordinate, possibilities in list_of_possibilities:
        if coordinate not in coord_dict:
            coord_dict[coordinate] = (coordinate, possibilities)
        else:
            existing_coord, existing_possibilities = coord_dict[coordinate]
            
            # Skip [0] (filled cells) and empty lists when comparing
            existing_is_valid = existing_possibilities != [0] and len(existing_possibilities) > 0
            new_is_valid = possibilities != [0] and len(possibilities) > 0
            
            # Prefer valid lists over invalid ones
            if new_is_valid and not existing_is_valid:
                coord_dict[coordinate] = (coordinate, possibilities)
            # If both valid, keep the one with MORE possibilities (intersection would be ideal, but this is simpler)
            elif new_is_valid and existing_is_valid:
                # Actually for counting occurrences, we want to keep all possibilities
                # So keep the longer list
                if len(possibilities) > len(existing_possibilities):
                    coord_dict[coordinate] = (coordinate, possibilities)
    
    list_of_possibilities = list(coord_dict.values())

    #print(f"Possibitlies for cell ({row_idx},{col_idx}) neighbors = {list_of_possibilities} - {len(list_of_possibilities)}")

    occurences = {}
    for num in range(1,10):
        occurences[num] = 0

    for coordinate,values in list_of_possibilities:
        for item in values:
            if item == 0:
                pass
            else:
                occurences[item] += 1

    #print(occurences)

    key_rem = 0
    value_to_fill = 0
    for num in current_possibilities:
        #print(f"Value {num} has already have {occurences[num]} occurences")
        if occurences[num] == 0:
            key_rem +=1
            value_to_fill = num
    
    if key_rem == 1:
        if verbose:
            print('We have a unique cell!!')
        #print(f"----------------- {value_to_fill} is a solution for cell ({row_idx},{col_idx})")
        return value_to_fill
    else:
        return None
    

def solve_sudoku(grid, counter,total_to_fillin, verbose=False):
        
    if counter == total_to_fillin:
        if verbose:
            print(f"We're done!")
        success = True
        return grid, success

    options_grid = [[[0] for i in range(9)] for j in range(9)]

    for row_idx in range(len(grid)):
        for col_idx in range(len(grid[0])):

            cell_value = grid[row_idx][col_idx]
            
            possibilities = []

            # Check if value is already filled in, if not we proceed. 
            if cell_value != 0:
                options_grid[row_idx][col_idx] = [0]
                #print(f"Cell is already occupied ({row_idx},{col_idx})")
            else:
                for v in VALUES:
                    row = grid[row_idx]
                    col = [row[col_idx] for row in grid]
                    if (v not in row) and (v not in col):
                        possibilities.append(v)
                        possibilities = check_block(grid,possibilities,(row_idx,col_idx),verbose=verbose)
                
                #print(f"Possibilities are {possibilities} for cell ({row_idx},{col_idx})")
                options_grid[row_idx][col_idx] = possibilities

     # ...existing code...
    #print(f"grid options {counter}/{total_to_fillin}")
    #print_grid(options_grid)
    #print('sssssssssssssssss')

    fill_in_value = None
    for row_idx in range(len(grid)):
        for col_idx in range(len(grid[0])):

            cell_value = options_grid[row_idx][col_idx]

            if cell_value == [0]:
                pass
                # print('Cell already filled in')
            
            elif len(cell_value) == 1:
                fill_in_value = cell_value[0]
            else:
                fill_in_value = check_block_options(options_grid,(row_idx,col_idx), verbose=verbose)

            if fill_in_value == None:
                #print('Could not update cell')
                pass
            else:
                if verbose:
                    print(f"We can update cell ({row_idx},{col_idx}) with value {fill_in_value}")
                grid[row_idx][col_idx] = fill_in_value
                counter += 1
                if verbose:
                    print(f"Solved {counter} out of {total_to_fillin}")
                return solve_sudoku(grid, counter,total_to_fillin, verbose=verbose)
    
    if verbose:
        print("We're stuck here...")
    success = False
    return grid,success


if __name__ == '__main__':
    import templates as tpl

    test_grid = tpl.test_grid10
    start = time.time()
    counter = 0
    count_zeros = lambda grid: sum(row.count(0) for row in grid)
    total_to_fillin = count_zeros(test_grid)

    print_grid(test_grid)
    print('---------')
    solution, success_flag = solve_sudoku(test_grid, counter, total_to_fillin, verbose=True)
    print('---------')
    if success_flag:
        print("Final solution:")
    else:
        print("How far we got:")
    print_grid(solution)
    print('---------')
    end = time.time()
    if success_flag:
        print(f"Solve took {round(end-start,5)} seconds")
