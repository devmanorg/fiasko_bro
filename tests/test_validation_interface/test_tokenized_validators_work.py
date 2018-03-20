import os
import pytest

from .utils import initialize_repo
from fiasko_bro.validator_helpers import (
    tokenized_validator_run_if_any,
    tokenized_validator_run_if_all,
    tokenized_validator_run_if
)
from fiasko_bro import CodeValidator


MESSAGE = 'validator runs'


@pytest.fixture(scope='module')
def get_validator_with_single_token(token):
    @tokenized_validator_run_if(token)
    def tokenized_validator_with_single_token(solution_repo, *args, **kwargs):
        return MESSAGE,
    return tokenized_validator_with_single_token


@pytest.fixture(scope='module')
def get_validator_with_two_optional_tokens(iterable):
    @tokenized_validator_run_if_any(iterable)
    def tokenized_validator_with_two_optional_tokens(solution_repo, *args, **kwargs):
        return MESSAGE,
    return tokenized_validator_with_two_optional_tokens


@pytest.fixture(scope='module')
def get_validator_with_two_mandatory_tokens(iterable):
    @tokenized_validator_run_if_all(iterable)
    def tokenized_validator_with_two_mandatory_tokens(solution_repo, *args, **kwargs):
        return MESSAGE,
    return tokenized_validator_with_two_mandatory_tokens


@pytest.fixture(scope='module')
def code_validator():
    code_validator = CodeValidator()
    validator_with_single_token = get_validator_with_single_token('sqlalchemy')
    validator_with_two_optional_tokens = get_validator_with_two_optional_tokens({'minmax', 'maximize'})
    validator_with_two_mandatory_tokens = get_validator_with_two_mandatory_tokens(['django', 'twisted'])
    code_validator.error_validator_groups['commits'].append(validator_with_single_token)
    code_validator.error_validator_groups['commits'].append(validator_with_two_optional_tokens)
    code_validator.error_validator_groups['commits'].append(validator_with_two_mandatory_tokens)
    return code_validator


@pytest.fixture(scope='module')
def origin_repo():
    repo_path = 'test_fixtures{}general_repo_origin'.format(os.path.sep)
    initialize_repo(repo_path)
    return repo_path


def test_tokenized_validator_with_single_token_ok(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_token='sqlalchemy')
    assert (MESSAGE,) in output


def test_tokenized_validator_with_single_token_fail(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_token=None)
    assert (MESSAGE,) not in output


def test_tokenized_validator_with_optional_tokens_ok(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_tokens=['maximize', 'minmax', 'sql'])
    assert (MESSAGE,) in output


def test_tokenized_validator_with_optional_tokens_fail(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_tokens=['sql', 'concurrency'])
    assert (MESSAGE,) not in output


def test_validator_with_mandatory_tokens_ok(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_tokens=('twisted', 'django'))
    assert (MESSAGE,) in output


def test_validator_with_mandatory_tokens_fail(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_tokens={'django', 'tornado'})
    assert (MESSAGE,) not in output
