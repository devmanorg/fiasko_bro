import pytest

import git

from fiasko_bro.repository_info import LocalRepositoryInfo


@pytest.fixture(scope="module")
def test_repo():
    test_repo_dir = 'test_fixtures/general_repo'
    git.Repo.init(test_repo_dir)
    return LocalRepositoryInfo(test_repo_dir)


@pytest.fixture(scope="module")
def origin_repo():
    origin_repo_dir = 'test_fixtures/general_repo_origin'
    git.Repo.init(origin_repo_dir)
    return LocalRepositoryInfo(origin_repo_dir)


@pytest.fixture(scope='session')
def temp_dir_for_tests(tmpdir_factory):
    temp_repo_dir = tmpdir_factory.mktemp('temp_dir_for_test')
    git.Repo.init(temp_repo_dir)
    return temp_repo_dir
