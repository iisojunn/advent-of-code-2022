import sys


class File:
    def __init__(self, name, parent, size=0):
        self.name = name
        self.parent = parent
        self.size = int(size)

    def __repr__(self, depth=0):
        return '  ' * depth + f'{self.name} {self.size}'


class Directory(File):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = {}

    def increase_size(self, addition):
        self.size += int(addition)
        if self.parent:
            self.parent.increase_size(addition)

    def __repr__(self, depth=0):
        children = ""
        for child in self.children.values():
            children += "\n" + child.__repr__(depth + 1)
        return super().__repr__(depth) + children


def change_directory(command, current_dir, root_dir):
    _, target_dir = command.split(" ")
    if target_dir == "/":
        return root_dir
    if target_dir == '..':
        return current_dir.parent
    return current_dir.children[target_dir]


def handle_ls(command, current_dir):
    for dir_content in command.split("\n")[1:]:
        size, name = dir_content.strip().split(" ")
        if size == "dir":
            sub_object = Directory(name, current_dir)
        else:
            sub_object = File(name, current_dir, size)
            current_dir.increase_size(size)
        current_dir.children[name] = sub_object


def parse_filesystem_status(commands, root):
    current_dir = root
    for command in commands:
        command = command.strip()
        if command.startswith("cd"):
            current_dir = change_directory(command, current_dir, root)
        elif command.startswith("ls"):
            handle_ls(command, current_dir)


def directories_fulfilling(_function, directory):
    if _function(directory):
        yield directory.size
    for sub_dir in filter(lambda x: isinstance(x, Directory), directory.children.values()):
        yield from directories_fulfilling(_function, sub_dir)


def main():
    file_name = sys.argv[1]
    commands = input_content(file_name).split("$ ")
    root = Directory("/", None)
    parse_filesystem_status(commands, root)
    print(sum(directories_fulfilling(lambda x: x.size <= 100_000, root)))

    total_disk_space = 70_000_000
    required_free_space = 30_000_000
    free_disk_space = total_disk_space - root.size
    need_to_free_space = required_free_space - free_disk_space
    print(min(directories_fulfilling(lambda x: x.size >= need_to_free_space, root)))


def input_content(file_name):
    with open(file_name) as file:
        return file.read()


if __name__ == '__main__':
    main()
