from collections import deque
import sys
from dataclasses import dataclass
from itertools import takewhile


def main():
    file_name = sys.argv[1]
    crate_lines, instructions_lines = split_input_lines(raw_lines(file_name))
    ships = initialize_ships(crate_lines)
    move_crates(ships, instructions_lines)
    print(top_crates(ships))


def split_input_lines(line_generator):
    crate_lines = list(takewhile(not_empty_line, line_generator))
    instruction_lines = list(line_generator)
    return crate_lines, instruction_lines


def not_empty_line(x):
    return x != ""


def raw_lines(file_name):
    with open(file_name) as file:
        for line in file.readlines():
            yield line.rstrip()


def initialize_ships(crate_lines):
    ship_numbers_line = crate_lines.pop()
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


def move_crates(ships, instructions_lines):
    for line in instructions_lines:
        execute_instruction(ships, parse_instruction(line))


def execute_instruction(ships, instruction):
    for _ in range(instruction.amount):
        ships[instruction.to].append(ships[instruction.from_].pop())


def top_crates(ships):
    return "".join(ship.pop() for ship in ships.values())


if __name__ == '__main__':
    main()
