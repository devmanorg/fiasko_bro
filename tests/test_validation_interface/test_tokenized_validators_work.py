import os

import pytest

from ..utils import initialize_repo, remove_repo
from fiasko_bro import tokenized_validators
from fiasko_bro import defaults
from fiasko_bro import validate


def get_validator_with_single_token(token):
    @tokenized_validators.run_if(token)
    def tokenized_validator_with_single_token(*args, **kwargs):
        return ''
    return tokenized_validator_with_single_token


def get_validator_with_two_disjunct_tokens(iterable):
    @tokenized_validators.run_if_any(iterable)
    def tokenized_validator_with_two_disjunct_tokens(*args, **kwargs):
        return ''
    return tokenized_validator_with_two_disjunct_tokens


def get_validator_with_two_conjunct_tokens(iterable):
    @tokenized_validators.run_if_all(iterable)
    def tokenized_validator_with_two_conjuct_tokens(*args, **kwargs):
        return ''
    return tokenized_validator_with_two_conjuct_tokens


@pytest.fixture(scope='session')
def error_validator_groups():
    validator_with_single_token = get_validator_with_single_token(1)
    validator_with_two_disjunct_tokens = get_validator_with_two_disjunct_tokens({'minmax', 'maximize'})
    validator_with_two_conjunct_tokens = get_validator_with_two_conjunct_tokens(['django', 'twisted'])
    new_validators = (
        validator_with_single_token,
        validator_with_two_disjunct_tokens,
        validator_with_two_conjunct_tokens,
    )
    modified_error_validator_groups = defaults.ERROR_VALIDATOR_GROUPS.copy()
    modified_error_validator_groups['commits'] = modified_error_validator_groups['commits'] + new_validators
    return modified_error_validator_groups


@pytest.fixture(scope='session')
def origin_repo():
    repo_path = 'test_fixtures{}general_repo_origin'.format(os.path.sep)
    initialize_repo(repo_path)
    yield repo_path
    remove_repo(repo_path)


def test_tokenized_validator_with_single_token_ok(origin_repo, error_validator_groups):
    output = validate(origin_repo, validator_token=1, error_validator_groups=error_validator_groups)
    assert ('tokenized_validator_with_single_token', '') in output


def test_tokenized_validator_with_single_token_fail(origin_repo, error_validator_groups):
    output = validate(origin_repo, validator_token=None, error_validator_groups=error_validator_groups)
    assert ('tokenized_validator_with_single_token', '') not in output


def test_validator_with_two_disjunct_tokens_ok(origin_repo, error_validator_groups):
    output = validate(origin_repo, validator_tokens=['minmax', 'sql'], error_validator_groups=error_validator_groups)
    assert ('tokenized_validator_with_two_disjunct_tokens', '') in output


def test_validator_with_two_disjunct_tokens_fail(origin_repo, error_validator_groups):
    output = validate(origin_repo, validator_tokens=['sql', 'concurrency'], error_validator_groups=error_validator_groups)
    assert ('tokenized_validator_with_two_disjunct_tokens', '') not in output


def test_validator_with_two_conjunct_tokens_ok(origin_repo, error_validator_groups):
    output = validate(origin_repo, validator_tokens=('twisted', 'django'), error_validator_groups=error_validator_groups)
    assert ('tokenized_validator_with_two_conjuct_tokens', '') in output


def test_validator_with_two_conjunct_tokens_fail(origin_repo, error_validator_groups):
    output = validate(origin_repo, validator_tokens={'django', 'tornado'}, error_validator_groups=error_validator_groups)
    assert ('tokenized_validator_with_two_conjuct_tokens', '') not in output


def test_mark_repo_with_both_fail(origin_repo):
    token = 'django'
    tokens = ('djano', 'celery')
    with pytest.raises(ValueError):
        validate(origin_repo, validator_token=token, validator_tokens=tokens)
