import os


def count_py_files(directory, directories_to_skip):
    all_files = []
    for directory, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [
            d for d in dirs
            if d not in directories_to_skip
        ]
        all_files += files
    return len([f for f in all_files if f.endswith('.py')])


def get_line_offsets(file_content):
    lines_offsets = [None]
    for line in file_content.split('\n'):
        lines_offsets.append(len(line) - len(line.lstrip(' ')))
    return lines_offsets


def is_in_utf8(name):
    if not (name.endswith('.py') or name.endswith('.txt')):
        return True
    try:
        with open((name), mode='r', encoding='utf-8') as file_handle:
            file_handle.read()
    except UnicodeDecodeError:
        return False
    return True


def is_file_too_long(file_path, max_number_of_lines):
    with open(file_path, 'r', encoding='utf-8') as file_handler:
        number_of_lines = 0
        while number_of_lines < max_number_of_lines and bool(file_handler.readline()):
            number_of_lines += 1
    return number_of_lines == max_number_of_lines
