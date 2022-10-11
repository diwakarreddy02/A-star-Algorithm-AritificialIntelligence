#!/usr/local/bin/python3
# solve_birds.py : Bird puzzle solver
#
# Code by: Venkata Diwakar Reddy Kashireddy vkashir
#
# Based on skeleton code by D. Crandall & B551 course staff, Fall 2022
#
# N birds stand in a row on a wire, each wearing a t-shirt with a number.
# In a single step, two adjacent birds can swap places. How can
# they rearrange themselves to be in order from 1 to N in the fewest
# possible steps?

# !/usr/bin/env python3
import sys

import time as t

#Importing PriorityQueue from queqe
from queue import PriorityQueue

#start_time = t.time()

N=5

#####
# THE ABSTRACTION:
#
# Initial state:

# Goal state:
# given a state, returns True or False to indicate if it is the goal state
def is_goal(state):
    return state == list(range(1, N+1))

# Successor function:
# given a state, return a list of successor states
def successors(state):
    return [ state[0:n] + [state[n+1],] + [state[n],] + state[n+2:] for n in range(0, N-1) ]

# Heuristic function:
# given a state, return an estimate of the number of steps to a goal from that state
# Here, we're taking heuristic funcition as number of birds with misplaced positions
def h(state):
    count = 0
    curr_state = state      
    g_state = list(range(1, N+1))
    for i in range(0, N):
        if curr_state[i] != g_state[i]:
            count += 1
    return count


#########
# THE ALGORITHM: A*, initiated Fringe as PriorityQueue, and then getting the state that has low f(s) value.  
#
def solve(initial_state):

    fringe = PriorityQueue()
    cost = 0

    fringe.put((cost,initial_state,[]),)

    while fringe:

        (cost, state, path) = fringe.get()
        
        if is_goal(state):
            return path+[state,]

        for s in successors(state):
            #print("Succerssor States are: ", s)
            fringe.put((h(state) + (cost + 1), s, path+[state,]))

    return []

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a test case filename"))

    test_cases = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            test_cases.append([ int(i) for i in line.split() ])
    print("Test Cases are:", test_cases)
    for initial_state in test_cases:
        	print('From state ' + str(initial_state) + " found goal state by taking path: " + str(solve(initial_state)))


#print("Total Time Taken: ", t.time()-start_time)







# #!/usr/local/bin/python3
# # solve_birds.py : Bird puzzle solver
# #
# # Code by: name IU ID
# #
# # Based on skeleton code by D. Crandall & B551 course staff, Fall 2022
# #
# # N birds stand in a row on a wire, each wearing a t-shirt with a number.
# # In a single step, two adjacent birds can swap places. How can
# # they rearrange themselves to be in order from 1 to N in the fewest
# # possible steps?

# # !/usr/bin/env python3
# import sys

# import time as t

# start_time = t.time()

# N=5

# #####
# # THE ABSTRACTION:
# #
# # Initial state:

# # Goal state:
# # given a state, returns True or False to indicate if it is the goal state
# def is_goal(state):
#     return state == list(range(1, N+1))

# # Successor function:
# # given a state, return a list of successor states
# def successors(state):
#     return [ state[0:n] + [state[n+1],] + [state[n],] + state[n+2:] for n in range(0, N-1) ]


# # # Heuristic function:
# # # given a state, return an estimate of the number of steps to a goal from that state
# # Here, we're taking heuristic funcition as Number of misplaced positions

# def h(state):
#     count = 0
#     curr_state = state      
#     g_state = list(range(1, N+1))
#     for i in range(0, N):
#         if curr_state[i] != g_state[i]:
#             count += 1
#     return count


# def rem_ele(fringe):
#     item =[None]
#     min_value = 9999
#     for i in fringe:
#         #print("\n\n i in f_fringe", i)
#         g = i[0]
#         x = h(i[1])
#         min_sum = x + g
#         if min_sum < min_value:
#             min_value = min_sum
#             item  = i
#     fringe.remove(item) 
#     return fringe, item


\
# #########
# #
# # THE ALGORITHM:
# #
# # This is a generic solver using BFS. 
# #
# def solve(initial_state):
#     fringe = []
#     cost = 0 

#     fringe += [(cost, initial_state, []),]
#     while len(fringe) > 0:
#         fringe, (cost, state, path) = rem_ele(fringe)
        
#         if is_goal(state):
#             return path+[state,]

#         for s in successors(state):
#             fringe.append((cost+1, s, path+[state,]))

#     return []

# # Please don't modify anything below this line
# #
# if __name__ == "__main__":
#     if(len(sys.argv) != 2):
#         raise(Exception("Error: expected a test case filename"))

#     test_cases = [[5,4,3,2,1]]
#     # with open(sys.argv[1], 'r') as file:
#     #     for line in file:
#     #         test_cases.append([ int(i) for i in line.split() ])
#     for initial_state in test_cases:
#         	print('From state ' + str(initial_state) + " found goal state by taking path: " + str(solve(initial_state)))

# print("Total Time Taken: ", t.time()-start_time)
