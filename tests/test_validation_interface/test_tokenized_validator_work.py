import os
import pytest

from .utils import initialize_repo
from fiasko_bro.validator_helpers import tokenized_validator
from fiasko_bro import CodeValidator


@tokenized_validator(['always_give_error'])
def get_error_always_validator(solution_repo, *args, **kwargs):
    return 'always error',


@tokenized_validator(['token_a', 'token_b'])
def get_error_always_validator_with_two_tokens(solution_repo, *args, **kwargs):
    return 'always error with two tokens',


@pytest.fixture(scope='module')
def code_validator():
    code_validator = CodeValidator()
    code_validator.error_validator_groups['commits'].append(get_error_always_validator)
    code_validator.error_validator_groups['commits'].append(get_error_always_validator_with_two_tokens)
    return code_validator


@pytest.fixture(scope='module')
def origin_repo():
    repo_path = 'test_fixtures{}general_repo_origin'.format(os.path.sep)
    initialize_repo(repo_path)
    return repo_path


def test_tokenized_validator_ok(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_token='always_give_error')
    assert ('always error',) in output


def test_tokenized_validator_fail(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_token=None)
    assert ('always error',) not in output


def test_tokenized_validator_with_mult_tokens_ok(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_token=['other_token', 'token_b'])
    assert ('always error with two tokens',) in output


def test_tokenized_validator_with_mult_tokens_fail(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_token=['other_token', 'token_c'])
    assert ('always error with two tokens',) not in output
