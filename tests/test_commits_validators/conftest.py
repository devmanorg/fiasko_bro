import os.path

import pytest
import git

from fiasko_bro.repository_info import ProjectFolder
from fiasko_bro import defaults


@pytest.fixture(scope="module")
def test_repo():
    test_repo_dir = 'test_fixtures{}commits_repo'.format(os.path.sep)
    repo = git.Repo.init(test_repo_dir)
    repo.index.add(['initial_file.py'])
    repo.index.commit('Initial commit')
    repo.index.add(['second_commit_file.py'])
    repo.index.commit('win')
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    return ProjectFolder(test_repo_dir, directories_to_skip)


@pytest.fixture(scope="module")
def origin_repo():
    origin_repo_dir = 'test_fixtures{}commits_repo_origin'.format(os.path.sep)
    repo = git.Repo.init(origin_repo_dir)
    repo.index.add(['initial_file.py'])
    repo.index.commit('Initial commit')
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    return ProjectFolder(origin_repo_dir, directories_to_skip)
