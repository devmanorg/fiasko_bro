import os.path

import pytest

from fiasko_bro import validate


@pytest.fixture(scope='session')
def non_existent_directory():
    directory = 'test_fixtures{}directory_that_should_not_exist'.format(os.path.sep)
    assert not os.path.isdir(directory)
    return directory


def test_not_existing_file_raises_correct_exception(non_existent_directory):
    with pytest.raises(FileNotFoundError):
        validate(non_existent_directory)
