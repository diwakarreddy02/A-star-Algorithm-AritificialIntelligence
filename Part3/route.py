#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: kaur94
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#


# !/usr/bin/env python3
import sys
from math import tanh, radians, cos, sin, asin, sqrt


def parse_city_gps():
    d1 = {}
    with open('city-gps.txt', 'r') as file:
        for line in file.readlines():
            l1 = line.split(" ")
            l1[-1] = float(l1[-1].strip())
            l1[-2] = float(l1[-2])
            d1[l1[0].strip()] = (l1[-2], l1[-1])
    file.close()
    return d1


def parse_road_segments():
    d1 = {}
    with open('road-segments.txt', 'r') as file:
        for line in file.readlines():
            l1 = line.split(" ")
            # Length in miles.
            l1[2] = float(l1[2])
            # Speed limit in miles/hour.
            l1[3] = float(l1[3])
            l1[-1] = l1[-1].strip()
            key = l1[0]
            subkey = l1[1]
            if key in d1:
                d1[key][subkey] = l1[2:]
            else:
                subdict = {subkey: l1[2:]}
                d1[key] = subdict
            key, subkey = subkey, key
            if key in d1:
                d1[key][subkey] = l1[2:]
            else:
                subdict = {subkey: l1[2:]}
                d1[key] = subdict
    file.close()
    return d1


def get_node_index_with_min_total_cost(fringe):
    min_cost = -1
    min_index = -1
    for i in range(len(fringe)):
        if fringe[i][3] < min_cost or min_cost == -1:
            min_cost = fringe[i][3]
            min_index = i
    return min_index


def find_max_speed(road_segments_dict):
    max_speed = 0
    for key, values in road_segments_dict.items():
        for sub_key, sub_values in values.items():
            if road_segments_dict[key][sub_key][1] > max_speed:
                max_speed = road_segments_dict[key][sub_key][1]
    return max_speed


def get_distance(start_cords, end_cords):
    lat_start_radian = radians(start_cords[0])
    long_start_radian = radians(start_cords[1])
    lat_end_radian = radians(end_cords[0])
    long_end_radian = radians(end_cords[1])

    delta_lat = lat_end_radian - lat_start_radian
    delta_long = long_end_radian - long_start_radian
    earth_radius_miles = 3958.8
    return round((2 * asin(sqrt(sin(delta_lat / 2) ** 2 + cos(lat_start_radian) * cos(lat_end_radian) * sin(delta_long / 2) ** 2))) * earth_radius_miles, 3)


def get_route_by_segments_cost(start, end):
    road_segments_dict = parse_road_segments()
    # nodes_visited is of the format {curr_node: prev_node, ...}
    nodes_visited = {}
    # Heuristic -> Possible minimum number of segments leading to goal: 1 (a constant)
    fringe = [(None, start, 0, 1)]
    # fringe -> [(prev_node, curr_node, cost_to_reach_the_node, total_cost=cost_to_reach_the_node+heuristic_cost)]
    while len(fringe) > 0:
        # Get node with minimum cost from the fringe.
        prev_node, curr_node, curr_cost, total_cost = fringe.pop(get_node_index_with_min_total_cost(fringe))
        if curr_node in nodes_visited:
            continue
        nodes_visited[curr_node] = prev_node

        if curr_node == end:
            route_taken = []
            total_segments = 0
            total_miles = 0.0
            total_hours = 0.0
            total_delivery_hours = 0.0
            if nodes_visited[curr_node] is not None:
                # Trace the path.
                curr = curr_node
                while nodes_visited[curr] is not None:
                    route_details = road_segments_dict[nodes_visited[curr]][curr]
                    segment_info = f"{route_details[2]} for {route_details[0]} miles"
                    route_taken.insert(0, (curr, segment_info))
                    curr = nodes_visited[curr]
                start = curr
                for elem in route_taken:
                    end = elem[0]
                    route_details = road_segments_dict[start][end]
                    dist = route_details[0]
                    total_miles += dist
                    speed = route_details[1]
                    if speed >= 50:
                        # Compute probability
                        t_trip = total_hours
                        t_road = dist / speed
                        p = tanh(dist / 1000)
                        total_delivery_hours += (t_road + (p * 2 * (t_road + t_trip)))
                    else:
                        total_delivery_hours += dist / speed
                    total_hours += dist / speed
                    start = end
                total_segments = len(route_taken)

            return {"total-segments": total_segments,
                    "total-miles": total_miles,
                    "total-hours": total_hours,
                    "total-delivery-hours": total_delivery_hours,
                    "route-taken": route_taken}

        # Traverse through all the adjacent nodes of curr_node.
        adjacent_nodes_dict = road_segments_dict[curr_node]
        for key, value in adjacent_nodes_dict.items():
            if key in nodes_visited:
                continue
            next_node = key
            next_node_cost = curr_cost + 1
            # If a node is not present in city-gps.txt we assume the heuristic cost is 0.
            next_node_heuristic_cost = 1
            next_node_total_cost = next_node_cost + next_node_heuristic_cost
            fringe.append((curr_node, next_node, next_node_cost, next_node_total_cost))


def get_route_by_distance_cost(start, end):
    city_gps_dict = parse_city_gps()
    road_segments_dict = parse_road_segments()
    # nodes_visited is of the format {curr_node: prev_node, ...}
    nodes_visited = {}
    start_node_cords = city_gps_dict[start]
    end_node_cords = city_gps_dict[end]
    # Heuristic -> Euclidean distance between 2 cities.
    fringe = [(None, start, 0, get_distance(start_node_cords, end_node_cords))]
    # fringe -> [(node, cost_to_reach_the_node, total_cost=cost_to_reach_the_node+heuristic_cost)]
    while len(fringe) > 0:
        # Get node with minimum cost from the fringe.
        prev_node, curr_node, curr_cost, total_cost = fringe.pop(get_node_index_with_min_total_cost(fringe))
        if curr_node in nodes_visited:
            continue
        nodes_visited[curr_node] = prev_node

        if curr_node == end:
            route_taken = []
            total_segments = 0
            total_miles = 0.0
            total_hours = 0.0
            total_delivery_hours = 0.0
            if nodes_visited[curr_node] is not None:
                # Trace the path.
                curr = curr_node
                while nodes_visited[curr] is not None:
                    route_details = road_segments_dict[nodes_visited[curr]][curr]
                    segment_info = f"{route_details[2]} for {route_details[0]} miles"
                    route_taken.insert(0, (curr, segment_info))
                    curr = nodes_visited[curr]
                start = curr
                for elem in route_taken:
                    end = elem[0]
                    route_details = road_segments_dict[start][end]
                    dist = route_details[0]
                    total_miles += dist
                    speed = route_details[1]
                    if speed >= 50:
                        # Compute probability
                        t_trip = total_hours
                        t_road = dist / speed
                        p = tanh(dist / 1000)
                        total_delivery_hours += (t_road + (p * 2 * (t_road + t_trip)))
                    else:
                        total_delivery_hours += dist / speed
                    total_hours += dist / speed
                    start = end
                total_segments = len(route_taken)

            return {"total-segments": total_segments,
                    "total-miles": total_miles,
                    "total-hours": total_hours,
                    "total-delivery-hours": total_delivery_hours,
                    "route-taken": route_taken}

        # Traverse through all the adjacent nodes of curr_node.
        adjacent_nodes_dict = road_segments_dict[curr_node]
        for key, value in adjacent_nodes_dict.items():
            if key in nodes_visited:
                continue
            length = value[0]
            next_node = key
            next_node_cost = curr_cost + length
            # If a node is not present in city-gps.txt we assume the heuristic cost is 0.
            next_node_heuristic_cost = 0
            if curr_node in city_gps_dict and next_node in city_gps_dict:
                curr_node_cords = city_gps_dict[curr_node]
                next_node_cords = city_gps_dict[next_node]
                next_node_heuristic_cost = get_distance(curr_node_cords, next_node_cords)
            next_node_total_cost = next_node_cost + next_node_heuristic_cost
            fringe.append((curr_node, next_node, next_node_cost, next_node_total_cost))


def get_route_by_time_cost(start, end):
    city_gps_dict = parse_city_gps()
    road_segments_dict = parse_road_segments()
    # nodes_visited is of the format {curr_node: prev_node, ...}
    nodes_visited = {}
    max_speed = find_max_speed(road_segments_dict)
    start_node_cords = city_gps_dict[start]
    end_node_cords = city_gps_dict[end]
    # Heuristic: (Euclidean distance from current node to end node) / max_speed
    fringe = [(None, start, 0, get_distance(start_node_cords, end_node_cords) / max_speed)]
    # fringe -> [(node, cost_to_reach_the_node, total_cost=cost_to_reach_the_node+heuristic_cost)]
    while len(fringe) > 0:
        # Get node with minimum cost from the fringe.
        prev_node, curr_node, curr_cost, total_cost = fringe.pop(get_node_index_with_min_total_cost(fringe))
        if curr_node in nodes_visited:
            continue
        nodes_visited[curr_node] = prev_node
        if curr_node == end:
            route_taken = []
            total_segments = 0
            total_miles = 0.0
            total_hours = 0.0
            total_delivery_hours = 0.0
            if nodes_visited[curr_node] is not None:
                # Trace the path.
                curr = curr_node
                while nodes_visited[curr] is not None:
                    route_details = road_segments_dict[nodes_visited[curr]][curr]
                    segment_info = f"{route_details[2]} for {route_details[0]} miles"
                    route_taken.insert(0, (curr, segment_info))
                    curr = nodes_visited[curr]
                start = curr
                for elem in route_taken:
                    end = elem[0]
                    route_details = road_segments_dict[start][end]
                    dist = route_details[0]
                    total_miles += dist
                    speed = route_details[1]
                    if speed >= 50:
                        # Compute probability
                        t_trip = total_hours
                        t_road = dist / speed
                        p = tanh(dist / 1000)
                        total_delivery_hours += (t_road + (p * 2 * (t_road + t_trip)))
                    else:
                        total_delivery_hours += dist / speed
                    total_hours += dist / speed
                    start = end
                total_segments = len(route_taken)

            return {"total-segments": total_segments,
                    "total-miles": total_miles,
                    "total-hours": total_hours,
                    "total-delivery-hours": total_delivery_hours,
                    "route-taken": route_taken}

        # Traverse through all the adjacent nodes of curr_node.
        adjacent_nodes_dict = road_segments_dict[curr_node]
        for key, value in adjacent_nodes_dict.items():
            if key in nodes_visited:
                continue
            length = value[0]
            speed = value[1]
            next_node = key
            next_node_cost = curr_cost + (length / speed)
            # If a node is not present in city-gps.txt we assume the heuristic cost is 0.
            next_node_heuristic_cost = 0
            if curr_node in city_gps_dict and next_node in city_gps_dict:
                curr_node_cords = city_gps_dict[curr_node]
                next_node_cords = city_gps_dict[next_node]
                next_node_heuristic_cost = get_distance(curr_node_cords, next_node_cords) / max_speed
            next_node_total_cost = next_node_cost + next_node_heuristic_cost
            fringe.append((curr_node, next_node, next_node_cost, next_node_total_cost))


def get_route_by_delivery_cost(start, end):
    city_gps_dict = parse_city_gps()
    road_segments_dict = parse_road_segments()
    # nodes_visited is of the format {curr_node: prev_node, ...}
    nodes_visited = {}
    max_speed = find_max_speed(road_segments_dict)
    start_node_cords = city_gps_dict[start]
    end_node_cords = city_gps_dict[end]
    # Heuristic: (euclidean distance from current node to end node) / max_speed
    fringe = [(None, start, 0, get_distance(start_node_cords, end_node_cords) / max_speed, 0)]
    # fringe -> [(node, cost_to_reach_the_node, total_cost=cost_to_reach_the_node+heuristic_cost), total_time_so_far]
    while len(fringe) > 0:
        # Get node with minimum cost from the fringe.
        prev_node, curr_node, curr_cost, total_curr_cost, total_time = fringe.pop(get_node_index_with_min_total_cost(fringe))

        if curr_node in nodes_visited:
            continue
        nodes_visited[curr_node] = prev_node
        if curr_node == end:
            route_taken = []
            total_segments = 0
            total_miles = 0.0
            total_hours = 0.0
            total_delivery_hours = 0.0
            if nodes_visited[curr_node] is not None:
                # Trace the path.
                curr = curr_node
                while nodes_visited[curr] is not None:
                    route_details = road_segments_dict[nodes_visited[curr]][curr]
                    segment_info = f"{route_details[2]} for {route_details[0]} miles"
                    route_taken.insert(0, (curr, segment_info))
                    curr = nodes_visited[curr]
                start = curr
                for elem in route_taken:
                    end = elem[0]
                    route_details = road_segments_dict[start][end]
                    dist = route_details[0]
                    total_miles += dist
                    speed = route_details[1]
                    if speed >= 50:
                        # Compute probability
                        t_trip = total_hours
                        t_road = dist / speed
                        p = tanh(dist / 1000)
                        total_delivery_hours += (t_road + (p * 2 * (t_road + t_trip)))

                    else:
                        total_delivery_hours += dist / speed
                    total_hours += dist / speed
                    start = end
                total_segments = len(route_taken)

            return {"total-segments": total_segments,
                    "total-miles": total_miles,
                    "total-hours": total_hours,
                    "total-delivery-hours": total_delivery_hours,
                    "route-taken": route_taken}

        # Traverse through all the adjacent nodes of curr_node.
        adjacent_nodes_dict = road_segments_dict[curr_node]
        for key, value in adjacent_nodes_dict.items():
            if key in nodes_visited:
                continue
            length = value[0]
            speed = value[1]
            next_node = key
            next_node_cost = curr_cost
            if speed >= 50:
                # Compute probability
                t_trip = total_time
                t_road = length / speed
                p = tanh(length / 1000)
                next_node_cost += (t_road + (p * 2 * (t_road + t_trip)))
            else:
                next_node_cost += length / speed

            next_node_total_time = total_time + length / speed
            # If a node is not present in city-gps.txt we assume the heuristic cost is 0.
            next_node_heuristic_cost = 0
            if curr_node in city_gps_dict and next_node in city_gps_dict:
                curr_node_cords = city_gps_dict[curr_node]
                next_node_cords = city_gps_dict[next_node]
                next_node_heuristic_cost = get_distance(curr_node_cords, next_node_cords) / max_speed
            next_node_total_cost = next_node_cost + next_node_heuristic_cost
            fringe.append((curr_node, next_node, next_node_cost, next_node_total_cost, next_node_total_time))


def get_route(start, end, cost):
    if cost == "segments":
        return get_route_by_segments_cost(start, end)
    if cost == "distance":
        return get_route_by_distance_cost(start, end)
    if cost == "time":
        return get_route_by_time_cost(start, end)
    if cost == "delivery":
        return get_route_by_delivery_cost(start, end)


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
