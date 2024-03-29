import operator
import sys
from functools import cmp_to_key, reduce
from itertools import zip_longest


def read_input(filename):
    with open(filename) as file:
        return file.read()


def packets(data):
    for packet in filter(lambda x: bool(x), data.split("\n")):
        yield eval(packet)


def pairs(data):
    packet_it = iter(packets(data))
    for index, pair in enumerate(zip(packet_it, packet_it)):
        yield index + 1, pair


class CorrectOrder(Exception):
    pass


class IncorrectOrder(Exception):
    pass


class ComparisonFailed(Exception):
    pass


class OutOfItems:
    pass


def compare_integers(left, right):
    if left < right:
        raise CorrectOrder
    elif left > right:
        raise IncorrectOrder


def compare_lists(left, right):
    for left_packet, right_packet in zip_longest(left, right, fillvalue=OutOfItems):
        compare(left_packet, right_packet)


def compare(left, right):
    if type(left) == int and type(right) == int:
        compare_integers(left, right)
    elif type(left) == list and type(right) == list:
        compare_lists(left, right)
    elif left == OutOfItems:
        raise CorrectOrder
    elif right == OutOfItems:
        raise IncorrectOrder
    elif type(left) == int:
        compare([left], right)
    elif type(right) == int:
        compare(left, [right])
    else:
        raise ComparisonFailed


def is_right_order(pair):
    left, right = pair
    try:
        compare(left, right)
    except CorrectOrder:
        return True
    except IncorrectOrder:
        return False
    raise ComparisonFailed


def packet_comparer(packet, other):
    return -1 if is_right_order((packet, other)) else 1


def main():
    data = read_input(sys.argv[1])
    print(sum(index for index, pair in pairs(data) if is_right_order(pair)))

    dividers = [[[2]], [[6]]]
    unordered_signal = list(packets(data)) + dividers
    signal = sorted(unordered_signal, key=cmp_to_key(packet_comparer))
    divider_indices = (signal.index(packet) + 1 for packet in dividers)
    print(reduce(operator.mul, divider_indices))


if __name__ == '__main__':
    main()
