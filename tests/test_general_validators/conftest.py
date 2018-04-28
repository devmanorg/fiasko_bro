import os.path

import pytest

from tests.utils import initialize_repo, remove_repo
from fiasko_bro import defaults
from fiasko_bro.repository_info import ProjectFolder


@pytest.fixture(scope="session")
def test_repo():
    test_repo_dir = 'test_fixtures{}general_repo'.format(os.path.sep)
    remove_repo(test_repo_dir)
    initialize_repo(test_repo_dir, ignore_gitignore=True)
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    yield ProjectFolder(test_repo_dir, directories_to_skip)
    remove_repo(test_repo_dir)


@pytest.fixture(scope="session")
def origin_repo():
    origin_repo_dir = 'test_fixtures{}general_repo_origin'.format(os.path.sep)
    remove_repo(origin_repo_dir)
    initialize_repo(origin_repo_dir)
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    yield ProjectFolder(origin_repo_dir, directories_to_skip)
    remove_repo(origin_repo_dir)
