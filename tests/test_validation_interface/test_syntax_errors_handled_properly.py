import os.path

import pytest

from .utils import initialize_repo
from fiasko_bro import validate_repo


@pytest.fixture(scope="module")
def syntax_error_repo():
    repo_path = 'test_fixtures{}syntax_error_repo'.format(os.path.sep)
    initialize_repo(repo_path)
    return repo_path


def test_warnings_show_up_after_fail(syntax_error_repo):
    expected_output = [
        ('syntax_error', 'file_with_syntax_error.py')
    ]
    output = validate_repo(syntax_error_repo)
    assert output == expected_output
