import sys


def move_tail(head, tail):
    if touching(head, tail):
        return tail

    vertical = head[0] - tail[0]
    if vertical > 0:
        tail = right(tail)
    elif vertical < 0:
        tail = left(tail)

    horizontal = head[1] - tail[1]
    if horizontal > 0:
        tail = down(tail)
    elif horizontal < 0:
        tail = up(tail)

    return tail


def surroundings(point):
    yield from (
        up(point),
        up(right(point)),
        right(point),
        right(down(point)),
        down(point),
        down(left(point)),
        left(point),
        left(up(point)),
    )


def touching(head, tail):
    return head == tail or any(head == around for around in surroundings(tail))


def right(point):
    return point[0] + 1, point[1]


def up(point):
    return point[0], point[1] - 1


def left(point):
    return point[0] - 1, point[1]


def down(point):
    return point[0], point[1] + 1


MOVE_FUNCTIONS = {
    "R": right,
    "U": up,
    "L": left,
    "D": down,
}


def visited_locations_for_tail(instructions):
    head, tail = (0, 0), (0, 0)
    visited_locations = {tail}
    for move, amount in instructions:
        for _ in range(amount):
            head = move(head)
            tail = move_tail(head, tail)
            visited_locations.update([tail])
    return visited_locations


def read_instructions(filename):
    with open(filename) as file:
        for line in file.readlines():
            direction, amount = line.split()
            yield MOVE_FUNCTIONS[direction], int(amount)


def main():
    instructions = read_instructions(sys.argv[1])
    visited_locations = visited_locations_for_tail(instructions)
    print(len(visited_locations))


if __name__ == '__main__':
    main()
