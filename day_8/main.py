import operator
import sys
from functools import reduce


def read_input(filename):
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]


def left_side(tree_map, x, y):
    for _x in range(x - 1, -1, -1):
        yield tree_map[_x][y]


def right_side(tree_map, x, y):
    for _x in range(x + 1, len(tree_map)):
        yield tree_map[_x][y]


def up_side(tree_map, x, y):
    for _y in range(y - 1, -1, -1):
        yield tree_map[x][_y]


def down_side(tree_map, x, y):
    for _y in range(y + 1, len(tree_map[0])):
        yield tree_map[x][_y]


def is_visible_from(side, tree_map, x, y):
    tree_lengths = tuple(side(tree_map, x, y))
    if not tree_lengths:
        return True
    return tree_map[x][y] > max(tree_lengths)


def all_directions():
    return left_side, up_side, right_side, down_side


def is_visible(tree_map, x, y):
    for direction in all_directions():
        if is_visible_from(direction, tree_map, x, y):
            return True
    return False


def visible_trees(tree_map):
    for x in range(len(tree_map)):
        for y in range(len(tree_map[0])):
            if is_visible(tree_map, x, y):
                yield x, y


def visibility_to_one_direction(direction, tree_map, x, y):
    height = tree_map[x][y]
    visibility = 0
    for tree in direction(tree_map, x, y):
        visibility += 1
        if tree >= height:
            break
    return visibility


def visibility_to_all_directions(tree_map, x, y):
    for direction in all_directions():
        yield visibility_to_one_direction(direction, tree_map, x, y)


def single_scenic_score(tree_map, x, y):
    return reduce(operator.mul, visibility_to_all_directions(tree_map, x, y))


def scenic_scores(tree_map):
    for x in range(len(tree_map)):
        for y in range(len(tree_map[0])):
            yield single_scenic_score(tree_map, x, y)


def main():
    filename = sys.argv[1]
    tree_map = read_input(filename)
    print(len(tuple(visible_trees(tree_map))))
    print(max(scenic_scores(tree_map)))


if __name__ == '__main__':
    main()
