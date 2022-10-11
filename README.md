# Assignment 1

## Part 1

- From the problem statement, five birds, each wearing a different number from 1 to N are sitting on a power line. They start in a random order and their      goal is to re-arrange themselves to be in order from 1 to N (e.g., 12345), in as few steps as possible.   

**Shortcomings of the Skeleton code:**
-From the given code, the algorihtm used is BFS and run time is very slow.


1. Here, A* search is implemented in place of BFS(from skeleton code). 
2. We initialized Fringe as PriorityQueue, then we added a tuple -> (cost, initial_state, path) to the fringe.
      Here, cost = g(s) = Cost that took to reach an intermediate state. 
            path = Each intermediate state to reach final state.
3. h(s) = Number of birds with misplaced positions. The heuristic is admissible because if current state is not goal state, then the minimun number of                 moves to reach goal state will not be less than this.
   - Initialized a function h(state) to get the heuristic of an intermediate/current state.
   - Here, we checked the current state birds position with the goal state to get the number of birds that are at wrong positions. 
   - Once, we go the count, we returned the count value.
4. **Procedure to reach goal state**
   1. Add the initial_state to the fringe priority queue
   2. While, the fringe is not empty, Pop the the state that has the minimun f(s), i.e., g(s) + h(s). Funtion h(s) gets the heuristic value for that state. 
   4. If goal state is reached, return the part.
   5. If not then, get the successors(next intermediate states) of the recently poped fringe, and add them to the priority queue. 
   6. Repeat steps 2 - 4 until goal state is reached.
   
## Part 2

- In the given problem, there is a 5 x 5 board with 25 tiles on it. It is similar to a 9-puzzle but with no empty spots. The goal is to achieve the desired board configuration by sliding the rows or columns (or) by rotating the inner or outer rings.
      **Goal State:** [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18.19,20],[21,22,23,24,25]]

1. The goal is to find the shortest path from the initial state to the goal state so **A* search** has been used.
2. Successor states are stored using **Priority Queue** to pick the best successor state by finding the cost to move to next state.
       - As there are 5 rows or coulmns that can be rotated, all their successor states are looped but the outer or inner rings can rotate only once so they need not be looped.
      - **heapq** module is used to represent the priority queue as it helps prioritize the state with lowest cost.
      - The cost is h(s) + g(s), where h(s) is the heuristic function and g(s) is the length so far from the initial state.  
3. **Algorithm**
      - Initialize an empty fringe. 
      - Add a dictionary to track whether a state has been visited or not.
      - Insert starting elements into fringe.
      - If fringe is not empty, pop out elements from the fringe.
      - Get all the possible successor states from current state.
      - If successor state is the goal state, return the current path plus the final move
      - If the state has not been visited, add it to the visited dict
      - Push next set of elements into the fringe.

_Question 1: In this problem, what is the branching factor of the search tree?_


Ans: Branching factor is the number of successors of each state. In this case, each state has 24 successors so **the branching factor is 24.**

**Question 2: If the solution can be reached in 7 moves, about how many states would we need to explore before we
found it if we used BFS instead of A* search?**

Ans: BFS explores all the successors before moving to the next stage. So for the 2nd move it explores 24 * 1 = 24 states, for the 3rd move it explores 24 * 2 = 48 states and so on. 
As the solution is reached in 7 moves, the number of states explored would be 24 * (1 + 2 + 3 + 4 + 5 + 6) = 24 * 21 = **504 states**


## Part 3

1. Used A* search for minimizing the cost depending on the cost type. Minimized (g(s) + h(s)) for every cost type, where g(s) is the cost so far and h(s) is the heuristic cost to goal. 
   1. **Cost: segments**
      1. g(s) = Number of segments traversed to reach the current state.
      2. h(s) = Minimum possible number of segments that can lead to goal state from current state = 1 (a constant)
      3. The heuristic is admissible because if current state is not goal state, 1 is the minimum number of segments required to reach goal state. It can be more than this but never less than 1.
   2. **Cost: distance**
      1. g(s) = Number of miles travelled by road to reach the current state.
      2. h(s) = Euclidean distance from current state to goal state.
      3. The heuristic is admissible because euclidean distance is the minimum distance to reach from point a to point b in space. The actual distance can be equal or more to this but never less than this.
   3. **Cost: time**
      1. g(s) = Amount of time required to reach the current state.
      2. h(s) = Minimum amount of time in which one can reach to goal state from the current state = Euclidean distance from current state to goal state / Maximum speed in whole of the data set.
      3. The heuristic is admissible because euclidean distance is the minimum distance to reach from point a to point b in space, and we are taking the maximum speed possible in whole of the dataset to calculate the minimum time. The actual time can be equal or more to this but never less than this.
   4. **Cost: delivery**
      1. g(s) = Amount of delivery time estimated to reach the current state.
      2. h(s) = Minimum amount of time in which one can reach to goal state from the current state = Euclidean distance from current state to goal state / Maximum speed in whole of the data set.
      3. The heuristic used in cost: delivery is same as cost: time, and it is admissible because delivery time can be equal or greater than time (without any extra trips required for delivery) and since h(s) for cost: time is admissible for cost: time, it will be admissible for cost: delivery.
2. **Parameters**
   1. **State space:** For any city / node that is visited, all its adjacent nodes are part of the fringe along with the adjacent nodes of previously visited nodes. A node is popped from the fringe when it is visited.
   2. **Successor function:** All the nodes present in the fringe are compared and the one with the minimum cost (depending upon the cost type) is selected.
   3. **Edge weights:**
      1. **Cost: segments** - Edge weight is 1 for all segments.
      2. **Cost: distance** - Edge weight is the length / distance of that segment.
      3. **Cost: time** - Edge weight is the time (given by - distance of the segment / speed limit of that segment) of that segment.
      4. **Cost: delivery** - Edge weight is the estimated delivery time (given by time of that segment + extra time based on some probability) of that segment.
   4. **Goal state:** The path that lead from start city to end city while minimizing the given cost type.
3. **How algorithm works**
   1. Append the start state to the fringe.
   2. Pop the node with minimum cost from the fringe.
   3. Mark the popped node as visited and current_node.
   4. Check if it's goal node, if yes - return.
   5. Compute cost (given by g(s) + h(s)) for all the adjacent nodes of the current_node and append to fringe.
   6. Repeat steps 2-5 until goal state is reached or all the nodes are visited.
4. **Assumptions and approximations**
   1. road-segments.txt has some nodes (cities, highway names, etc.) which are not present in city-gps.txt. Since latitude and longitude are not present for these nodes, h(s) cannot be computed when euclidean distance is involved (as in where cost is distance, time or delivery) so it is assumed to be 0.
