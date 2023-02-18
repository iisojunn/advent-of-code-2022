import sys
from collections import deque


def main():
    file_name = sys.argv[1]
    signals = tuple(read_input(file_name))
    for signal in signals:
        print(start_marker_position(signal))


def read_input(file_name):
    with open(file_name) as file:
        for line in file.readlines():
            yield line.strip()


def start_marker_position(signal, marker_length=4):
    buffer = deque(signal[:marker_length])
    for position, char in enumerate(signal[marker_length:], start=marker_length):
        if is_all_different(buffer):
            return position
        buffer.popleft()
        buffer.append(char)


def is_all_different(string):
    return len(set(string)) == len(string)


if __name__ == '__main__':
    main()
