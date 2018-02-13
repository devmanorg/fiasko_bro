import os.path

import pytest
import git

from fiasko_bro.repository_info import LocalRepositoryInfo


@pytest.fixture(scope="module")
def test_repo():
    test_repo_dir = 'test_fixtures{}general_repo'.format(os.path.sep)
    git.Repo.init(test_repo_dir)
    return LocalRepositoryInfo(test_repo_dir)


@pytest.fixture(scope="module")
def origin_repo():
    origin_repo_dir = 'test_fixtures{}general_repo_origin'.format(os.path.sep)
    git.Repo.init(origin_repo_dir)
    return LocalRepositoryInfo(origin_repo_dir)
