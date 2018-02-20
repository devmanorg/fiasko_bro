import os.path

import pytest
import git

from fiasko_bro.repository_info import LocalRepositoryInfo


@pytest.fixture(scope="module")
def test_repo():
    test_repo_dir = 'test_fixtures{}syntax_repo'.format(os.path.sep)
    git.Repo.init(test_repo_dir)
    return LocalRepositoryInfo(test_repo_dir)


@pytest.fixture(scope="module")
def control_repo():
    control_repo_dir = 'test_fixtures{}general_repo'.format(os.path.sep)
    git.Repo.init(control_repo_dir)
    return LocalRepositoryInfo(control_repo_dir)
