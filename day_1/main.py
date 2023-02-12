import argparse
from collections import defaultdict


def read_input(file_name):
    with open(file_name, 'r') as file:
        return (line.strip() for line in file.readlines())


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", type=str, default="test_input")
    args = parser.parse_args()
    return args


def parse_data(data):
    elves_food = defaultdict(int)
    elf = 0
    for calories in data:
        if not calories:
            elf += 1
            continue
        elves_food[elf] += int(calories)
    return elves_food


def main():
    args = cli()
    elves_food = parse_data(read_input(args.input_file))
    print(max(elves_food.values()))
    sorted_food_count = sorted(elves_food.values(), reverse=True)
    print(sum(sorted_food_count[:3]))


if __name__ == '__main__':
    main()
