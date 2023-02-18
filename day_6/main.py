import sys
from collections import deque


def main():
    file_name = sys.argv[1]
    signals = tuple(read_input(file_name))
    for signal in signals:
        print(detect_distinct_marker_position(signal, distinct_length=4))
    for signal in signals:
        print(detect_distinct_marker_position(signal, distinct_length=14))


def read_input(file_name):
    with open(file_name) as file:
        for line in file.readlines():
            yield line.strip()


def detect_distinct_marker_position(signal, distinct_length):
    buffer = deque(signal[:distinct_length])
    for position, char in enumerate(signal[distinct_length:], start=distinct_length):
        if is_all_different(buffer):
            return position
        buffer.popleft()
        buffer.append(char)


def is_all_different(string):
    return len(set(string)) == len(string)


if __name__ == '__main__':
    main()
