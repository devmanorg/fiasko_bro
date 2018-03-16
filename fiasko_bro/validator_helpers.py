from functools import wraps


def tokenized_validator(list_of_tokens):
    def validator_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            repo_tokens = kwargs.get('validator_token')
            if repo_tokens:
                if [token for token in list_of_tokens if token in repo_tokens]:
                    return func(*args, **kwargs)
        return func_wrapper
    return validator_decorator
