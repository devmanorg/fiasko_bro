import os.path

import pytest

from fiasko_bro import defaults
from fiasko_bro.repository_info import ProjectFolder


@pytest.fixture(scope="module")
def test_repo():
    test_repo_dir = 'test_fixtures{}general_repo'.format(os.path.sep)
    directories_to_skip = defaults.VALIDATOR_SETTINGS['directories_to_skip']
    return ProjectFolder(test_repo_dir, directories_to_skip)


@pytest.fixture(scope="module")
def origin_repo():
    origin_repo_dir = 'test_fixtures{}general_repo_origin'.format(os.path.sep)
    directories_to_skip = defaults.VALIDATOR_SETTINGS['directories_to_skip']
    return ProjectFolder(origin_repo_dir, directories_to_skip)
