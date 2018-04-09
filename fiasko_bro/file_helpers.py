import os

from fiasko_bro.defaults import VALIDATOR_SETTINGS


def count_py_files(directory):
    all_files = []
    for directory, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [
            d for d in dirs
            if d not in VALIDATOR_SETTINGS['directories_to_skip']
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
