from functools import wraps


def tokenized_validator(token):
    def validator_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            if token == kwargs.get('validator_token'):
                return func(*args, **kwargs)
        return func_wrapper
    return validator_decorator
