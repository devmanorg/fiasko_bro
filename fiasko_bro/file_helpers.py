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


def is_in_utf8(name):
    if not (name.endswith('.py') or name.endswith('.txt')):
        return True
    try:
        with open((name), mode='r', encoding='utf-8') as file_handle:
            file_handle.read()
    except UnicodeDecodeError:
        return False
    return True


def is_filename_in_whitelist(file_name, whitelist):
    for whitelisted_part in whitelist:
        if whitelisted_part in file_name:
            return True
    return False
