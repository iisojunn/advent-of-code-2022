import string
import sys


def split_into_two(input_string):
    half = int(len(input_string) / 2)
    return input_string[:half], input_string[-half:]


def raw_data(file_name):
    with open(file_name) as file:
        for line in file.readlines():
            yield line.strip()


def rucksacks(file_name):
    for line in raw_data(file_name):
        yield split_into_two(line)


def group_bags(file_name):
    iterator = iter(raw_data(file_name))
    while True:
        try:
            yield next(iterator), next(iterator), next(iterator)
        except StopIteration:
            break


def priority(item):
    return string.ascii_letters.index(item) + 1


def sum_of_priorities(items):
    return sum(priority(item) for item in items)


def main():
    file_name = sys.argv[1]
    common_items = [
        set(compartment_a).intersection(set(compartment_b)).pop()
        for compartment_a, compartment_b in rucksacks(file_name)
    ]
    print(sum_of_priorities(common_items))

    common_badges = [
        set(bag_a).intersection(bag_b).intersection(bag_c).pop()
        for bag_a, bag_b, bag_c in group_bags(file_name)
    ]
    print(sum_of_priorities(common_badges))


if __name__ == '__main__':
    main()
