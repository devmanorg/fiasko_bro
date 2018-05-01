from functools import wraps
from ..utils.validator_helpers import if_any, if_all, if_in


def run_if_tokens_satisfy_condition(tokens, condition):
    def validator_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            repo_token = kwargs.get('validator_token')
            if repo_token is not None:
                repo_token = [repo_token]
            repo_tokens = repo_token or kwargs.get('validator_tokens')
            if repo_tokens and condition(tokens, repo_tokens):
                return func(*args, **kwargs)
        return func_wrapper
    return validator_decorator


def run_if_any(tokens):
    return run_if_tokens_satisfy_condition(tokens, if_any)


def run_if_all(tokens):
    return run_if_tokens_satisfy_condition(tokens, if_all)


def run_if(token):
    return run_if_tokens_satisfy_condition(token, if_in)
