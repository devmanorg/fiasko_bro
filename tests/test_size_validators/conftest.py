import os.path
import pytest



@pytest.fixture(scope="session")
def general_repo_origin_path():
    general_repo_origin_dir = 'test_fixtures{}general_repo_origin'.format(os.path.sep)
    return general_repo_origin_dir


@pytest.fixture(scope="session")
def general_repo_path():
    general_repo_dir = 'test_fixtures{}general_repo'.format(os.path.sep)
    return general_repo_dir
