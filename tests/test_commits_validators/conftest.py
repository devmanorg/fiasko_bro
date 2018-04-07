import os.path

import pytest
import git

from fiasko_bro.repository_info import ProjectFolder


@pytest.fixture(scope="module")
def test_repo():
    test_repo_dir = 'test_fixtures{}commits_repo'.format(os.path.sep)
    repo = git.Repo.init(test_repo_dir)
    repo.index.add(['initial_file.py'])
    repo.index.commit('Initial commit')
    repo.index.add(['second_commit_file.py'])
    repo.index.commit('win')
    return ProjectFolder(test_repo_dir)


@pytest.fixture(scope="module")
def origin_repo():
    origin_repo_dir = 'test_fixtures{}commits_repo_origin'.format(os.path.sep)
    repo = git.Repo.init(origin_repo_dir)
    repo.index.add(['initial_file.py'])
    repo.index.commit('Initial commit')
    return ProjectFolder(origin_repo_dir)
