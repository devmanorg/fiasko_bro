from stdlib_list import stdlib_list


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def get_stdlibs_list(python_version='3.5'):
    return [l.split('.')[0] for l in stdlib_list(python_version)]
