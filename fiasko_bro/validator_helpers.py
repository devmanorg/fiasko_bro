def ensure_repo_tokens_mutually_exclusive(**kwargs):
    if 'validator_token' in kwargs and 'validator_tokens' in kwargs:
        raise ValueError("Please specify either 'token' or 'tokens'")


def if_any(tokens, repo_tokens):
    return any(token for token in tokens if token in repo_tokens)


def if_all(tokens, repo_tokens):
    return set(tokens) == set(repo_tokens)
