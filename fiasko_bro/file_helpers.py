import os


def count_py_files(directory):
    counter = 0
    for _, _, filenames in os.walk(directory):
        for name in filenames:
            if name.endswith('.py'):
                counter += 1
    return counter


def is_file_in_whitelist(file_path, whitelist):
    for whitelisted_part in whitelist:
        if whitelisted_part in file_path:
            return True
    return False


def get_line_offsets(file_content):
    lines_offsets = [None]
    for line in file_content.split('\n'):
        lines_offsets.append(len(line) - len(line.lstrip(' ')))
    return lines_offsets
