#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
# Code by: neneer@iu.edu
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022
#

# Correct indices for all the cells - will be used to calculate manhattan distance

import sys
import heapq

ROWS=5
COLS=5

actual_position = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3), 5: (0,4), 6: (1,0), 7:(1,1), 8:(1,2), 9:(1,3),
                    10:(1,4), 11:(2,0), 12:(2,1), 13:(2,2), 14:(2,3), 15:(2,4), 16:(3,0), 17:(3,1), 18:(3,2),
                    19:(3,3), 20:(3,4), 21:(4,0), 22:(4,1), 23:(4,2), 24:(4,3), 25:(4,4)}



# Return the value of row and column from index
def index(i):
    return (int(i/5), i % 5)


# Slide the row to left and wrap around
def slide_left(row):
    return row[1:] + row[0:1]

# Slide the row to right and wrap around
def slide_right(row):
    return row[-1:] + row[0:-1]

# Slide the column up and wrap around
def slide_up(col):
    return col[1:] + col[0:1]

# Slide the column down and wrap around
def slide_down(col):
    return col[-1:] + col[0:-1]

# Rotate outer ring clockwise and wrap around
def rotate_oc(state):
    return (tuple([state[5]]) + tuple(state[0:4]) + tuple([state[10]]) + tuple(state[6:9]) + tuple([state[4]]) + tuple([state[15]]) + tuple(state[11:14]) + tuple([state[9]]) + tuple([state[20]]) + tuple(state[16:19]) + tuple([state[14]]) + tuple([state[21]]) + tuple(state[22:25]) + tuple([state[19]]))

# Rotate outer ring counterclockwise and wrap around
def rotate_occ(state):
    return (tuple([state[1]]) + tuple(state[2:5]) + tuple([state[9]]) + tuple([state[0]]) + tuple(state[6:9]) + tuple([state[14]]) + tuple([state[5]]) + tuple(state[11:14]) + tuple([state[19]]) + tuple([state[10]]) + tuple(state[16:19]) + tuple([state[24]]) + tuple([state[15]]) + tuple(state[20:23]) + tuple([state[23]]))


# Rotate inner ring clockwise and wrap around
def rotate_ic(state):
    return (tuple(state[0:6]) + tuple([state[11]]) + tuple(state[6:8]) + tuple(state[9:11]) + tuple([state[16]]) + tuple([state[12]]) + tuple([state[8]]) + tuple(state[14:16]) + tuple(state[17:19]) + tuple([state[13]]) + tuple(state[19:]))


# Rotate inner ring counterclockwise and wrap around
def rotate_icc(state):
    return (tuple(state[0:6]) + tuple(state[7:9]) + tuple([state[13]]) + tuple(state[9:11]) + tuple([state[6]]) + tuple([state[12]]) + tuple([state[18]]) + tuple(state[14:16]) + tuple([state[11]]) + tuple(state[16:18]) + tuple(state[19:]))

# Successors of rotating the rows to left
def successors_left(state, row):
    rotated_row = slide_left(state[row*5:(row*5)+5])
    return (tuple(state[0:row*5] + rotated_row + state[(row*5)+5:]))


# Successors of rotating the row to right
def successors_right(state, row):
    rotated_row = slide_right(state[row*5:(row*5)+5])
    return (tuple(state[0:row*5] + rotated_row + state[(row*5)+5:]))


# Successors of rotating a column up
def successors_up(state, col):
    rotated_col = slide_up(state[col:col+21:5])
    return (tuple(state[0:col] + tuple([rotated_col[0]])) + state[col+1:col+5] + tuple([rotated_col[1]]) + state[col+6:col+10] + tuple([rotated_col[2]]) + state[col+11:col+15] + tuple([rotated_col[3]]) + state[col+16:col+20] + tuple([rotated_col[4]]) + state[col+21:])


# Successors of rotating a column down
def successors_down(state,col):
    rotated_col = slide_down(state[col:col + 21:5])
    return (tuple(state[0:col] + tuple([rotated_col[0]])) + state[col + 1:col + 5] + tuple([rotated_col[1]]) + state[col + 6:col + 10] + tuple([rotated_col[2]]) + state[col + 11:col + 15] + tuple([rotated_col[3]]) + state[col + 16:col + 20] + tuple([rotated_col[4]]) + state[col + 21:])


# Calculate Manhattan distance for each cell
def manhattan_cell(current_row, current_col, actual_row, actual_col):
    return abs(current_row - actual_row) + abs(current_col - actual_col)


# Calculate Manhattan distance for the total board
def manhattan_board(state):
    total = 0
    for i, val in enumerate(state):
        row, col = index(i)
        total += manhattan_cell(row,col, actual_position[val][0], actual_position[val][1])
    return total


def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]


# return a list of possible successor states
def successors(state):
    list = []

    for i in range(0, 5):
        list.append(
            [(successors_left(state, i)), 'L' + str(i + 1), manhattan_board(successors_left(state, i))])
        list.append(
            [(successors_right(state, i)), 'R' + str(i + 1), manhattan_board(successors_right(state, i))])
        list.append(
            [(successors_up(state, i)), 'U' + str(i + 1), manhattan_board(successors_up(state, i))])
        list.append(
            [(successors_down(state, i)), 'D' + str(i + 1), manhattan_board(successors_down(state, i))])
    list.append([(rotate_oc(state)), 'Oc', manhattan_board(rotate_oc(state))])
    list.append([(rotate_occ(state)), 'Occ', manhattan_board(rotate_occ(state))])
    list.append([(rotate_ic(state)), 'Ic', manhattan_board(rotate_ic(state))])
    list.append([(rotate_icc(state)), 'Icc', manhattan_board(rotate_icc(state))])

    return list



# check if we've reached the goal
def is_goal(state):
    # Goal achieved if sorted state is equal to the current state
    return sorted(state) == list(state)




def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    visited_states = {tuple(initial_board):True}
    fringe = []

    current_path = []
    current_cost = 0

    heapq.heappush(fringe, (manhattan_board(initial_board), (initial_board, current_cost, current_path)))

    while fringe:
        _, (state, current_cost, current_path) = heapq.heappop(fringe)
        for (next_state, move, manhattan_cost) in successors(state):
            if is_goal(next_state):
                return current_path + [move]
            else:
                if next_state not in visited_states.keys():
                    visited_states[next_state] = True
                    heuristic_val = current_cost + 1 + manhattan_cost
                    heapq.heappush(fringe, (heuristic_val, (next_state, current_cost + 1, current_path + [move])))

    return False




# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
