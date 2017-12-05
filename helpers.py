from functools import wraps

from stdlib_list import stdlib_list


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def get_stdlibs_list(python_version='3.5'):
    return [l.split('.')[0] for l in stdlib_list(python_version)]


def tokenized_validator(token):
    def validator_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            if token == kwargs.get('validator_token'):
                return func(*args, **kwargs)
            else:
                return True, None, None
        return func_wrapper
    return validator_decorator


def is_url_with_params(string):
    if not string.startswith('http') or '?' not in string:
        return False
    query_part = string.split('?')[-1]
    for key_value_pair in query_part.split('&'):
        if '=' not in key_value_pair:
            return False
    return True
