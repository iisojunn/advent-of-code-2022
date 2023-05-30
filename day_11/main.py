import operator
import sys
from collections import deque
from functools import reduce


class Monkey:
    def __init__(self, number, items, operation, divisor, true_monkey, false_monkey):
        self.number = number
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.test = test_generator(divisor)
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspection_count = 0

    def __repr__(self):
        return f"Monkey {self.number}: items {list(self.items)}, inspections: {self.inspection_count}"

    def take_turn(self, worry_level_divider):
        to_true_monkey = deque()
        to_false_monkey = deque()
        while self.items:
            item = self.items.popleft()
            self.inspection_count += 1
            item = self.operation(item)
            item = worry_level_divider(item)
            if self.test(item):
                to_true_monkey.append(item)
            else:
                to_false_monkey.append(item)
        return {
            self.true_monkey: to_true_monkey,
            self.false_monkey: to_false_monkey
        }

    @staticmethod
    def from_file_input(string):
        lines = string.split("\n")
        number = int(lines[0].replace("Monkey ", "").replace(":", ""))
        items = deque(int(item) for item in lines[1].replace("  Starting items: ", "").replace(" ", "").split(","))
        operation = operation_generator(lines[2].split("= ")[1])
        divisor = int(lines[3].replace("Test: divisible by ", ""))
        true_monkey = int(lines[4].split(" ")[-1])
        false_monkey = int(lines[5].split(" ")[-1])
        return Monkey(number, items, operation, divisor, true_monkey, false_monkey)


def operation_generator(definition):
    def operation(value):
        return eval(definition.replace('old', str(value)))

    return operation


def test_generator(number):
    def divisible_by(value):
        return value % number == 0

    return divisible_by


def read_input(filename):
    with open(filename) as file:
        return file.read()


def parse_monkeys(data):
    monkeys = []
    for monkey_data in data.split("\n\n"):
        monkeys.append(Monkey.from_file_input(monkey_data))
    return dict((monkey.number, monkey) for monkey in monkeys)


def grab_items(monkeys, thrown_items):
    for to_monkey, items in thrown_items.items():
        monkeys[to_monkey].items.extend(items)


def play_round(monkeys, worry_level_divider):
    for monkey in monkeys.values():
        thrown_items = monkey.take_turn(worry_level_divider)
        grab_items(monkeys, thrown_items)


def most_active_monkeys(monkeys, count=2):
    sorted_monkeys = sorted(list(monkeys.values()), key=lambda x: x.inspection_count, reverse=True)
    return sorted_monkeys[:count]


def monkey_business(monkeys):
    return reduce(operator.mul, (monkey.inspection_count for monkey in most_active_monkeys(monkeys)))


def common_denominator(monkeys):
    return reduce(operator.mul, (monkey.divisor for monkey in monkeys.values()))


def main():
    data = read_input(sys.argv[1])
    monkeys = parse_monkeys(data)
    for _ in range(20):
        play_round(monkeys, worry_level_divider=lambda x: int(x / 3))
    print(monkey_business(monkeys))

    monkeys = parse_monkeys(data)
    for round_ in range(10000):
        play_round(monkeys, worry_level_divider=lambda x: x % common_denominator(monkeys))
    print(monkey_business(monkeys))


if __name__ == '__main__':
    main()
