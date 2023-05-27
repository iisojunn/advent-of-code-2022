import operator
import sys
from functools import reduce
from itertools import product


def read_input(filename):
    with open(filename) as file:
        return [line.strip() for line in file.readlines()]


def to_zero(start):
    for value in range(start - 1, -1, -1):
        yield value


def left_side(tree_map, x, y):
    for _x in to_zero(x):
        yield tree_map[_x][y]


def right_side(tree_map, x, y):
    for _x in range(x + 1, len(tree_map)):
        yield tree_map[_x][y]


def up_side(tree_map, x, y):
    for _y in to_zero(y):
        yield tree_map[x][_y]


def down_side(tree_map, x, y):
    for _y in range(y + 1, len(tree_map[0])):
        yield tree_map[x][_y]


def is_visible_behind(trees, tree_height):
    try:
        tallest_tree = max(trees)
    except ValueError:
        return True
    return tree_height > tallest_tree


def all_directions():
    return left_side, up_side, right_side, down_side


def is_visible(tree_map, x, y):
    tree_height = tree_map[x][y]
    return any(is_visible_behind(direction(tree_map, x, y), tree_height) for direction in all_directions())


def visible_trees(tree_map):
    for x, y in all_coordinates(tree_map):
        if is_visible(tree_map, x, y):
            yield x, y


def all_coordinates(tree_map):
    return product(range(len(tree_map)), range(len(tree_map[0])))


def visibility_to_one_direction(trees, blocking_height):
    visibility = 0
    for tree_height in trees:
        visibility += 1
        if tree_height >= blocking_height:
            break
    return visibility


def visibility_to_all_directions(tree_map, x, y):
    height = tree_map[x][y]
    for direction in all_directions():
        yield visibility_to_one_direction(direction(tree_map, x, y), height)


def single_scenic_score(tree_map, x, y):
    return reduce(operator.mul, visibility_to_all_directions(tree_map, x, y))


def scenic_scores(tree_map):
    for x, y in all_coordinates(tree_map):
        yield single_scenic_score(tree_map, x, y)


def main():
    filename = sys.argv[1]
    tree_map = read_input(filename)
    print(len(tuple(visible_trees(tree_map))))
    print(max(scenic_scores(tree_map)))


if __name__ == '__main__':
    main()
