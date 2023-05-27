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


def visited_locations_for_tail(instructions, rope_length=2):
    rope = [(0, 0) for _ in range(rope_length)]
    visited_locations = {rope[-1]}
    for move, amount in instructions:
        for _ in range(amount):
            rope[0] = move(rope[0])
            for i in range(1, rope_length):
                rope[i] = move_tail(rope[i - 1], rope[i])
            visited_locations.update([rope[-1]])
    return visited_locations


def read_instructions(filename):
    with open(filename) as file:
        for line in file.readlines():
            direction, amount = line.split()
            yield MOVE_FUNCTIONS[direction], int(amount)


def main():
    instructions = list(read_instructions(sys.argv[1]))
    visited_locations = visited_locations_for_tail(instructions)
    print(len(visited_locations))
    visited_locations2 = visited_locations_for_tail(instructions, 10)
    print(len(visited_locations2))


if __name__ == '__main__':
    main()
