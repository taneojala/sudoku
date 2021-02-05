import numpy as np

# initialise (set initial values) (Page 1
# initial_grid = np.array([[0, 0, 0, 3, 0, 4, 0, 0, 0],
#                         [0, 1, 2, 5, 0, 8, 3, 4, 0],
#                         [0, 0, 3, 0, 7, 0, 9, 0, 0],
#                         [0, 2, 7, 1, 0, 6, 4, 9, 0],
#                         [0, 0, 0, 0, 4, 0, 0, 0, 0],
#                         [0, 6, 9, 7, 0, 3, 5, 2, 0],
#                         [0, 0, 1, 0, 3, 0, 2, 0, 0],
#                         [0, 7, 5, 4, 0, 9, 8, 6, 0],
#                         [0, 0, 0, 2, 0, 7, 0, 0, 0]]) # medium

initial_grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 3, 0, 1, 0, 0, 0],
                        [8, 0, 2, 0, 0, 0, 7, 0, 6],
                        [0, 8, 0, 0, 0, 0, 0, 6, 0],
                        [5, 0, 7, 0, 0, 0, 8, 0, 2],
                        [0, 0, 1, 0, 0, 0, 4, 0, 0],
                        [4, 9, 0, 7, 0, 2, 0, 8, 1],
                        [0, 1, 0, 8, 0, 9, 0, 7, 0],
                        [0, 7, 8, 0, 5, 0, 6, 4, 0]])  # page 199, difficult
#
# initial_grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
#                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                         [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                         [0, 0, 0, 0, 0, 0, 0, 0, 0]])   # silly

grid = initial_grid.copy()

presets = []
for x in range(9):
    for y in range(9):
        if initial_grid[x][y] != 0:
            presets.append({"x":x, "y":y})
free_positions = []
for x in range(9):
    for y in range(9):
        if initial_grid[x][y] == 0:
            free_positions.append({"x":x, "y":y})

def is_solved(grid):
    # return True if there's no zeros in grid
    return not 0 in grid

def is_preset(position):
    # returns True if the grid position was initially set already (fixed, that is)
    return position in presets

def validity(grid):
    for x in range(9):
        row = [grid[x][i] for i in range(9) if grid[x][i] > 0] # take non-zero numbers into row
        if len(row) != len(set(row)):   # compare if the length is equal to number of set's members
            return False   # if any row fails the whole grid fails
    return True

def is_legal_grid(grid):
    horizontal_validity = validity(grid)
    # transpose the original grid
    transposed_grid = grid.transpose()
    vertical_validity = validity(transposed_grid)
    # "transpose" 3*3 squares into nine 9*1 rows and do again
    squares_grid = []
    squares_grid.append(grid[0][0:3].tolist() + grid[1][0:3].tolist() + grid[2][0:3].tolist())
    squares_grid.append(grid[0][3:6].tolist() + grid[1][3:6].tolist() + grid[2][3:6].tolist())
    squares_grid.append(grid[0][6:9].tolist() + grid[1][6:9].tolist() + grid[2][6:9].tolist())
    squares_grid.append(grid[3][0:3].tolist() + grid[4][0:3].tolist() + grid[5][0:3].tolist())
    squares_grid.append(grid[3][3:6].tolist() + grid[4][3:6].tolist() + grid[5][3:6].tolist())
    squares_grid.append(grid[3][6:9].tolist() + grid[4][6:9].tolist() + grid[5][6:9].tolist())
    squares_grid.append(grid[6][0:3].tolist() + grid[7][0:3].tolist() + grid[8][0:3].tolist())
    squares_grid.append(grid[6][3:6].tolist() + grid[7][3:6].tolist() + grid[8][3:6].tolist())
    squares_grid.append(grid[6][6:9].tolist() + grid[7][6:9].tolist() + grid[8][6:9].tolist())
    three_by_three_validity = validity(squares_grid)
    return horizontal_validity and vertical_validity and three_by_three_validity

def next_position(position):
    if position in free_positions:
        if free_positions.index(position) == len(free_positions)-1:  # last item in list
            return {"x":-1, "y":-1}
        return free_positions[free_positions.index(position) + 1]
    return {"x": -1, "y": -1}

def previous_position(position):
    if position in free_positions:
        if position == free_positions[0]:   # first item
            return {"x":-1, "y":-1}
        return free_positions[free_positions.index(position) - 1]
    return {"x": -1, "y": -1}

def solve(grid, initpos, initvalue):    # position = {"x":0, "y":0}
    value = initvalue
    position = initpos  # the first cell that is originally empty
    i = 0
    while True: # value <= 9:
        i += 1
        grid[position["x"], position["y"]] = value
        if is_legal_grid(grid):
            position = next_position(position)
            if value != 1:  # since we found a legal value, we start anew from the start
                new_value = 1
            else:
                new_value = 2
            if is_solved(grid):
                print("Number of attempts: ", i)
                return grid
        else:    # undo the change - increase the value
            value = grid[position["x"], position["y"]]  # just to be sure
            grid[position["x"], position["y"]] = 0   # this may be unnecessary
            new_value = value + 1
        while new_value > 9:  # here we have reached a too big next value and need to back up
            grid[position["x"], position["y"]] = 0
            position = previous_position(position)
            new_value = grid[position["x"], position["y"]] + 1  # take the next value in the previous cell
        value = new_value

if __name__ == "__main__":
    print("Solving sudoku....")
    print(initial_grid)
    if not is_legal_grid(initial_grid):
        print("The provided grid is invalid")
    else:
        print("... wait!")
        solved_grid = solve(grid, free_positions[0], 1)
        print("Solved sudoku grid:")
        print(solved_grid)
