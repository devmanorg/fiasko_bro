import os
import pytest

from .utils import initialize_repo
from fiasko_bro import CodeValidator


@pytest.fixture(scope='module')
def code_validator():
    code_validator = CodeValidator()
    return code_validator


@pytest.fixture(scope='module')
def origin_repo():
    repo_path = 'test_fixtures{}general_repo_origin'.format(os.path.sep)
    initialize_repo(repo_path)
    return repo_path


def test_mark_repo_with_both(origin_repo, code_validator):
    token = 'django'
    tokens = ('djano', 'celery')
    with pytest.raises(ValueError):
        output = code_validator.validate(origin_repo, validator_token=token, validator_tokens=tokens)


def test_mark_repo_with_token_ok(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_token='django')


def test_mark_repo_with_tokens_ok(origin_repo, code_validator):
    output = code_validator.validate(origin_repo, validator_tokens=['tornado', 'sqlalchemy'])
