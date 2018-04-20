import os.path

import pytest

from .utils import initialize_repo
from fiasko_bro import validate


@pytest.fixture(scope="module")
def long_file_3_spaces_repo_path():
    repo_path = 'test_fixtures{}long_file_3_spaces_repo'.format(os.path.sep)
    initialize_repo(repo_path)
    return repo_path


def test_warnings_show_up_after_fail(long_file_3_spaces_repo_path):
    expected_output = [
        ('too_many_pep8_violations', '240 PEP8 violations'),
        ('long_file', 'long_file_3_spaces.py'),
        ('indent_not_multiple_of_tab_size', 'long_file_3_spaces.py:16')
    ]
    output = validate(long_file_3_spaces_repo_path)
    assert output == expected_output
