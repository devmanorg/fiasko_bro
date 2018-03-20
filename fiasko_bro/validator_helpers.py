from functools import wraps


def _general_tokenized_validator(tokens, check_method):
    def validator_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            repo_tokens = kwargs.get('validator_token')
            if repo_tokens is None:
                repo_tokens = kwargs.get('validator_tokens')
            if repo_tokens:
                if check_method(tokens, repo_tokens):
                    return func(*args, **kwargs)
        return func_wrapper
    return validator_decorator


def tokenized_validator_run_if_any(tokens):
    return _general_tokenized_validator(tokens, if_any)


def tokenized_validator_run_if_all(tokens):
    return _general_tokenized_validator(tokens, if_all)


def tokenized_validator_run_if(token):
    return _general_tokenized_validator(token, if_all)


def if_any(tokens, repo_tokens):
    return any(token for token in tokens if token in repo_tokens)


def if_all(tokens, repo_tokens):
    print(tokens, repo_tokens)
    return set(tokens) == set(repo_tokens)
