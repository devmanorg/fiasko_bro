import os


def count_py_files(directory):
    counter = 0
    for _, _, filenames in os.walk(directory):
        for name in filenames:
            if name.endswith('.py'):
                counter += 1
    return counter
