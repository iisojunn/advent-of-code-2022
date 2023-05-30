import sys


def signal_strengths(registry_history):
    for cycle in range(20, len(registry_history), 40):
        yield registry_history[cycle] * cycle


def simulate_execution(instructions):
    def register_to_history():
        history[len(history) + 1] = register

    register = 1
    history = {0: register}
    for line in instructions:
        register_to_history()
        if line != 'noop':
            register += int(line.split(" ")[1])
            register_to_history()
    return history


def read_instructions(filename):
    with open(filename) as file:
        for line in file.readlines():
            yield line.strip()


def main():
    instructions = read_instructions(sys.argv[1])
    registry_history = simulate_execution(instructions)
    print(sum(signal_strengths(registry_history)))


if __name__ == '__main__':
    main()
