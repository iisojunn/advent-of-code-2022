import math
import sys
from collections import defaultdict

import heapdict


def read_input(filename):
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]


def to_map(data):
    map2d = {}
    for x, row in enumerate(data):
        for y, spot in enumerate(row):
            map2d[(x, y)] = spot
    return map2d


def resolve_start_and_end(map2d):
    start, end = None, None
    for spot, value in map2d.items():
        if value == 'S':
            start = spot
        if value == 'E':
            end = spot
    return start, end


def to_elevation_map(map2d):
    elevation_map = {}
    for spot, value in map2d.items():
        if value == 'S':
            elevation = ord('a')
        elif value == 'E':
            elevation = ord('z')
        else:
            elevation = ord(value)
        elevation_map[spot] = elevation - ord('a')
    return elevation_map


def steps_for(spot, width, height):
    if spot[0] > 0:
        yield spot[0] - 1, spot[1]
    if spot[0] < width - 1:
        yield spot[0] + 1, spot[1]
    if spot[1] > 0:
        yield spot[0], spot[1] - 1
    if spot[1] < height - 1:
        yield spot[0], spot[1] + 1


def possible_steps_for_spot(elevation_map, width, height):
    for spot, elevation in elevation_map.items():
        for step in steps_for(spot, width, height):
            if elevation_map[step] <= elevation + 1:
                yield spot, step


def step_map(elevation_map, width, height, reverse=False):
    step_map_ = defaultdict(lambda: set())
    for spot, step in possible_steps_for_spot(elevation_map, width, height):
        if reverse:
            spot, step = step, spot
        step_map_[spot].add(step)
    return step_map_


def construct_path(previous, current):
    path = [current]
    while True:
        try:
            current = previous[current]
        except KeyError:
            return path
        path.append(current)


def dijkstra(all_spots, possible_steps, start, ends):
    distance = {start: 0}
    previous = {}
    priority_queue = heapdict.heapdict()
    for spot in all_spots:
        if spot != start:
            distance[spot] = math.inf
            previous[spot] = None
        priority_queue[spot] = distance[spot]

    while priority_queue:
        spot, dist = priority_queue.popitem()
        for next_spot in possible_steps[spot]:
            new_distance = dist + 1
            if new_distance < distance[next_spot]:
                distance[next_spot] = new_distance
                previous[next_spot] = spot
                priority_queue[next_spot] = new_distance
            if next_spot in ends:
                return construct_path(previous, next_spot)


def spots_with_elevation(elevation_map, elevation):
    return [spot for spot, value in elevation_map.items() if value == elevation]


def main():
    data = read_input(sys.argv[1])
    width = len(data)
    height = len(data[0])
    map2d = to_map(data)
    all_spots = list(map2d.keys())
    start, end = resolve_start_and_end(map2d)
    elevation_map = to_elevation_map(map2d)
    possible_steps = step_map(elevation_map, width, height)
    path = dijkstra(all_spots, possible_steps, start, [end])
    print(len(path) - 1)

    reverse_possible_steps = step_map(elevation_map, width, height, reverse=True)
    path = dijkstra(all_spots, reverse_possible_steps, end, spots_with_elevation(elevation_map, elevation=0))
    print(len(path) - 1)


if __name__ == '__main__':
    main()
