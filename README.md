# Assignment 1

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