import os.path

import pytest
import git

from tests.utils import remove_repo
from fiasko_bro.repository_info import ProjectFolder
from fiasko_bro import defaults


@pytest.fixture(scope="session")
def test_repo():
    test_repo_dir = 'test_fixtures{}commits_repo'.format(os.path.sep)
    remove_repo(test_repo_dir)
    repo = git.Repo.init(test_repo_dir)
    repo.index.add(['initial_file.py'])
    repo.index.commit('Initial commit')
    repo.index.add(['second_commit_file.py'])
    repo.index.commit('win')
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    yield ProjectFolder(test_repo_dir, directories_to_skip)
    remove_repo(test_repo_dir)


@pytest.fixture(scope="session")
def origin_repo():
    origin_repo_dir = 'test_fixtures{}commits_repo_origin'.format(os.path.sep)
    remove_repo(origin_repo_dir)
    repo = git.Repo.init(origin_repo_dir)
    repo.index.add(['initial_file.py'])
    repo.index.commit('Initial commit')
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    yield ProjectFolder(origin_repo_dir, directories_to_skip)
    remove_repo(origin_repo_dir)
