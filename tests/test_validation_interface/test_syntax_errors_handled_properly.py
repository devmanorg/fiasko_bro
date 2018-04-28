import os.path

import pytest

from tests.utils import initialize_repo, remove_repo
from fiasko_bro import validate


@pytest.fixture(scope="session")
def syntax_error_repo():
    repo_path = 'test_fixtures{}syntax_error_repo'.format(os.path.sep)
    remove_repo(repo_path)
    initialize_repo(repo_path)
    yield repo_path
    remove_repo(repo_path)


def test_syntax_error_shows_up(syntax_error_repo):
    expected_output = [
        ('syntax_error', 'file_with_syntax_error.py')
    ]
    output = validate(syntax_error_repo)
    assert output == expected_output
