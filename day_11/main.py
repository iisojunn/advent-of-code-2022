import operator
import sys
from collections import deque
from functools import reduce


class Monkey:
    def __init__(self, number, items, operation, test, true_monkey, false_monkey):
        self.number = number
        self.items = items
        self.operation = operation
        self.test = test
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspection_count = 0

    def __repr__(self):
        return f"Monkey {self.number}: items {list(self.items)}, inspections: {self.inspection_count}"

    def take_turn(self):
        to_true_monkey = deque()
        to_false_monkey = deque()
        while self.items:
            item = self.items.popleft()
            self.inspection_count += 1
            item = self.operation(item)
            item = int(item / 3)
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
        test = divisible_generator(int(lines[3].replace("Test: divisible by ", "")))
        true_monkey = int(lines[4].split(" ")[-1])
        false_monkey = int(lines[5].split(" ")[-1])
        return Monkey(number, items, operation, test, true_monkey, false_monkey)


def operation_generator(definition):
    def operation(value):
        return eval(definition.replace('old', str(value)))

    return operation


def divisible_generator(number):
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


def play_round(monkeys):
    for monkey in monkeys.values():
        thrown_items = monkey.take_turn()
        grab_items(monkeys, thrown_items)


def most_active_monkeys(monkeys, count=2):
    sorted_monkeys = sorted(list(monkeys.values()), key=lambda x: x.inspection_count, reverse=True)
    return sorted_monkeys[:count]


def main():
    data = read_input(sys.argv[1])
    monkeys = parse_monkeys(data)
    for _ in range(20):
        play_round(monkeys)
    monkey_business = reduce(operator.mul, (monkey.inspection_count for monkey in most_active_monkeys(monkeys)))
    print(monkey_business)


if __name__ == '__main__':
    main()
