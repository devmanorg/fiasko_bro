import os.path
import pytest



@pytest.fixture(scope="module")
def encoding_repo():
    encoding_repo_dir = 'test_fixtures{}encoding_repo'.format(os.path.sep)
    return encoding_repo_dir


@pytest.fixture(scope="module")
def general_repo():
    general_repo_dir = 'test_fixtures{}general_repo'.format(os.path.sep)
    return general_repo_dir
