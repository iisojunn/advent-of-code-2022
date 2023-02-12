import string
import sys


def split_into_two(input_string):
    half = int(len(input_string) / 2)
    return input_string[:half], input_string[-half:]


def rucksacks(file_name):
    with open(file_name) as file:
        for line in file.readlines():
            yield split_into_two(line.strip())


def priority(item):
    return string.ascii_letters.index(item) + 1


def main():
    file_name = sys.argv[1]
    common_items = [
        set(compartment_a).intersection(set(compartment_b)).pop()
        for compartment_a, compartment_b in rucksacks(file_name)
    ]
    print(sum((priority(item) for item in common_items)))


if __name__ == '__main__':
    main()
