import sys


def signal_strengths(registry_history):
    for cycle in range(20, len(registry_history), 40):
        yield registry_history[cycle] * cycle


def simulate_execution(instructions):
    register = 1
    history = [register]
    for line in instructions:
        history.append(register)
        if line != 'noop':
            register += int(line.split(" ")[1])
            history.append(register)
    return history


def read_instructions(filename):
    with open(filename) as file:
        for line in file.readlines():
            yield line.strip()


def render_row(sprite_locations):
    row = []
    for cursor, location in enumerate(sprite_locations):
        sprite = (location - 1, location, location + 1)
        row.append(cursor in sprite)
    return row


def render_screen(sprite_locations):
    screen = []
    for row_start in range(0, len(sprite_locations) - 1, 40):
        screen.append(render_row(sprite_locations[row_start:row_start + 40]))
    return screen


def print_screen(screen):
    for row in screen:
        for pixel in row:
            print("#" if pixel else " ", end='')
        print()


def main():
    instructions = list(read_instructions(sys.argv[1]))
    registry_history = simulate_execution(instructions)
    print(sum(signal_strengths(registry_history)))

    screen = render_screen(registry_history)
    print_screen(screen)


if __name__ == '__main__':
    main()
