from collections import deque
import sys
from dataclasses import dataclass
from itertools import takewhile


def main():
    file_name = sys.argv[1]
    crate_lines, ship_numbers_line, instructions_lines = split_input_lines(raw_lines(file_name))
    ships = initialize_ships(crate_lines, ship_numbers_line)
    move_crates(ships, instructions_lines, execute_instruction_crate_mover_9000)
    print(top_crates(ships))

    ships2 = initialize_ships(crate_lines, ship_numbers_line)
    move_crates(ships2, instructions_lines, execute_instruction_crate_mover_9001)
    print(top_crates(ships2))


def split_input_lines(line_generator):
    crate_lines = list(takewhile(not_empty_line, line_generator))
    ship_numbers_line = crate_lines.pop()
    instruction_lines = list(line_generator)
    return crate_lines, ship_numbers_line, instruction_lines


def not_empty_line(x):
    return x != ""


def raw_lines(file_name):
    with open(file_name) as file:
        for line in file.readlines():
            yield line.rstrip()


def initialize_ships(crate_lines, ship_numbers_line):
    ships = {int(number): deque() for number in ship_numbers_line.split("   ")}
    for crate_line in crate_lines:
        for ship, crate in zip(ships.values(), crate_line[1::4]):
            if crate != " ":
                ship.appendleft(crate)
    return ships


@dataclass
class Instruction:
    amount: int
    from_: int
    to: int


def parse_instruction(string):
    _, amount, _, from_, _, to = string.split(" ")
    return Instruction(int(amount), int(from_), int(to))


def move_crates(ships, instructions_lines, execute_instruction):
    for line in instructions_lines:
        execute_instruction(ships, parse_instruction(line))


def execute_instruction_crate_mover_9000(ships, instruction):
    for _ in range(instruction.amount):
        ships[instruction.to].append(ships[instruction.from_].pop())


def execute_instruction_crate_mover_9001(ships, instruction):
    crates = list(ships[instruction.from_].pop() for _ in range(instruction.amount))
    for crate in reversed(crates):
        ships[instruction.to].append(crate)


def top_crates(ships):
    return "".join(ship.pop() for ship in ships.values())


if __name__ == '__main__':
    main()
