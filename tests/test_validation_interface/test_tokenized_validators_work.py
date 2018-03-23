import os
import pytest

from .utils import initialize_repo
from fiasko_bro import tokenized_validators
from fiasko_bro import CodeValidator


MESSAGE_SINGLE_TOKEN = 'validator with single token ran'
MESSAGE_DISJUNCT_TOKENS = 'validator with two disjunct tokens ran'
MESSAGE_CONJUCT_TOKENS = 'validator with two conjuct tokens ran'


@pytest.fixture(scope='module')
def get_validator_with_single_token(token):
    @tokenized_validators.run_if(token)
    def tokenized_validator_with_single_token(solution_repo, *args, **kwargs):
        return MESSAGE_SINGLE_TOKEN,
    return tokenized_validator_with_single_token


@pytest.fixture(scope='module')
def get_validator_with_two_disjunct_tokens(iterable):
    @tokenized_validators.run_if_any(iterable)
    def tokenized_validator_with_two_disjunct_tokens(solution_repo, *args, **kwargs):
        return MESSAGE_DISJUNCT_TOKENS,
    return tokenized_validator_with_two_disjunct_tokens


@pytest.fixture(scope='module')
def get_validator_with_two_conjunct_tokens(iterable):
    @tokenized_validators.run_if_all(iterable)
    def tokenized_validator_with_two_conjuct_tokens(solution_repo, *args, **kwargs):
        return MESSAGE_CONJUCT_TOKENS,
    return tokenized_validator_with_two_conjuct_tokens


@pytest.fixture(scope='module')
def code_validator():
    code_validator = CodeValidator()
    validator_with_single_token = get_validator_with_single_token('sqlalchemy')
    validator_with_two_disjunct_tokens = get_validator_with_two_disjunct_tokens({'minmax', 'maximize'})
    validator_with_two_conjunct_tokens = get_validator_with_two_conjunct_tokens(['django', 'twisted'])
    code_validator.error_validator_groups['commits'].append(validator_with_single_token)
    code_validator.error_validator_groups['commits'].append(validator_with_two_disjunct_tokens)
    code_validator.error_validator_groups['commits'].append(validator_with_two_conjunct_tokens)
    return code_validator


@pytest.fixture(scope='module')
def origin_repo():
    repo_path = 'test_fixtures{}general_repo_origin'.format(os.path.sep)
    initialize_repo(repo_path)
    return repo_path


def test_tokenized_validator_with_single_token_ok(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_token='sqlalchemy')
    assert (MESSAGE_SINGLE_TOKEN,) in output


def test_tokenized_validator_with_single_token_fail(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_token=None)
    assert (MESSAGE_SINGLE_TOKEN,) not in output


def test_validator_with_two_disjunct_tokens_ok(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_tokens=['maximize', 'minmax', 'sql'])
    assert (MESSAGE_DISJUNCT_TOKENS,) in output


def test_validator_with_two_disjunct_tokens_fail(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_tokens=['sql', 'concurrency'])
    assert (MESSAGE_DISJUNCT_TOKENS,) not in output


def test_validator_with_two_conjunct_tokens_ok(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_tokens=('twisted', 'django'))
    assert (MESSAGE_CONJUCT_TOKENS,) in output


def test_validator_with_two_conjunct_tokens_fail(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_tokens={'django', 'tornado'})
    assert (MESSAGE_CONJUCT_TOKENS,) not in output


def test_mark_repo_with_both_fail(origin_repo, code_validator):
    token = 'django'
    tokens = ('djano', 'celery')
    with pytest.raises(ValueError):
        output = code_validator.validate(origin_repo, validator_token=token, validator_tokens=tokens)
