import os.path

import pytest

from tests.utils import initialize_repo
from fiasko_bro import validate


@pytest.fixture(scope="module")
def long_file_3_spaces_repo_path():
    repo_path = 'test_fixtures{}long_file_3_spaces_repo'.format(os.path.sep)
    initialize_repo(repo_path)
    return repo_path


def test_warnings_show_up_after_fail(long_file_3_spaces_repo_path):
    expected_output = [
        ('pep8', '240 PEP8 violations'),
        ('file_too_long', 'long_file_3_spaces.py'),
        ('indent_not_four_spaces', 'long_file_3_spaces.py:16')
    ]
    output = validate(long_file_3_spaces_repo_path)
    assert output == expected_output
