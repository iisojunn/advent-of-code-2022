import sys
from enum import Enum, auto
from itertools import pairwise, product


class Content(Enum):
    rock = auto()
    sand = auto()


def read_input(filename):
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]


def spots_between_corners(spot, other):
    x1, y1 = spot
    x2, y2 = other
    yield from product(range(min(x1, x2), max(x1, x2) + 1),
                       range(min(y1, y2), max(y1, y2) + 1))


def corners(scanning):
    for coordinates in scanning.split(" -> "):
        yield tuple(int(value) for value in coordinates.split(","))


def rock_spots_for(scanning):
    """Yields middle corners multiple times"""
    for corner, other in pairwise(corners(scanning)):
        yield from spots_between_corners(corner, other)


def all_rock_spots(data):
    for scanning in data:
        yield from rock_spots_for(scanning)


def construct_cave(data):
    return {spot: Content.rock for spot in all_rock_spots(data)}


def lowest_level(cave):
    return max(height for _, height in cave.keys())


class FellIntoAbyss(Exception):
    pass


class SandUnitStopped(Exception):
    pass


def possible_next_locations(sand_location):
    def down(t):
        return t[0], t[1] + 1

    def down_left(t):
        return t[0] - 1, t[1] + 1

    def down_right(t):
        return t[0] + 1, t[1] + 1

    for direction in (down, down_left, down_right):
        yield direction(sand_location)


def next_sand_location(cave, sand_location):
    for location in possible_next_locations(sand_location):
        if location not in cave.keys():
            return location
    raise SandUnitStopped


def add_sand_unit(cave, sand_source, abyss_level):
    sand_location = sand_source
    while True:
        try:
            sand_location = next_sand_location(cave, sand_location)
        except SandUnitStopped:
            break
        if sand_location[1] >= abyss_level:
            raise FellIntoAbyss
    cave[sand_location] = Content.sand


def fill_with_sand(cave, sand_source):
    abyss_level = lowest_level(cave)
    while True:
        try:
            add_sand_unit(cave, sand_source, abyss_level)
        except FellIntoAbyss:
            break


def main():
    data = read_input(sys.argv[1])
    cave = construct_cave(data)
    sand_source = (500, 0)
    fill_with_sand(cave, sand_source)
    print(len(list(content for content in cave.values() if content == Content.sand)))


if __name__ == '__main__':
    main()
