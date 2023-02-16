import sys


class Range:
    def __init__(self, string):
        lower, higher = string.split("-")
        self.lower = int(lower)
        self.higher = int(higher)

    def __repr__(self):
        return f"{self.lower}-{self.higher}"

    def contains(self, other):
        return self.lower <= other.lower and other.higher <= self.higher

    def overlaps(self, other):
        return self.lower <= other.lower <= self.higher or \
            self.lower <= other.higher <= self.higher or \
            other.lower <= self.lower <= other.higher or \
            other.lower <= self.higher <= other.higher


def section_ranges(file_name):
    with open(file_name) as file:
        for line in file.readlines():
            first, second = line.strip().split(",")
            yield Range(first), Range(second)


def main():
    file_name = sys.argv[1]
    contains_fully = 0
    for range_a, range_b in section_ranges(file_name):
        if range_a.contains(range_b) or range_b.contains(range_a):
            contains_fully += 1
    print(contains_fully)

    overlaps = 0
    for range_a, range_b in section_ranges(file_name):
        if range_a.overlaps(range_b):
            overlaps += 1
    print(overlaps)


if __name__ == '__main__':
    main()
