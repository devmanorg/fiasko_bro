import os.path
import pytest


@pytest.fixture(scope="session")
def encoding_repo_path():
    encoding_repo_dir = 'test_fixtures{}encoding_repo'.format(os.path.sep)
    return encoding_repo_dir


@pytest.fixture(scope="session")
def general_repo_path():
    general_repo_dir = 'test_fixtures{}general_repo'.format(os.path.sep)
    return general_repo_dir


@pytest.fixture(scope="session")
def test_repo_with_bom_path():
    test_repo_dir = 'test_fixtures{0}encoding_repo{0}utf8_with_bom'.format(os.path.sep)
    return test_repo_dir


@pytest.fixture(scope="session")
def test_repo_without_bom_path():
    test_repo_dir = 'test_fixtures{}general_repo'.format(os.path.sep)
    return test_repo_dir
