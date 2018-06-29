import os.path

import pytest

from tests.utils import initialize_repo, remove_repo
from fiasko_bro import validate


@pytest.fixture(scope="session")
def file_3_spaces_repo_path():
    repo_path = 'test_fixtures{}file_3_spaces_repo'.format(os.path.sep)
    remove_repo(repo_path)
    initialize_repo(repo_path)
    yield repo_path
    remove_repo(repo_path)


def test_warnings_show_up_after_fail(file_3_spaces_repo_path):
    expected_output = [
        ('too_many_pep8_violations', '43 PEP8 violations'),
        ('indent_not_multiple_of_tab_size', 'file_3_spaces.py:16')
    ]
    output = validate(file_3_spaces_repo_path)
    assert output == expected_output
