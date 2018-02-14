import os.path
from fiasko_bro.pre_validation_checks import are_repos_too_large


def test_repo_size_fail_single():
    max_py_files_count = 1
    path_to_repo = 'test_fixtures{}general_repo'.format(os.path.sep)
    output = are_repos_too_large(path_to_repo, max_py_files_count)
    assert isinstance(output, tuple)
    assert output[0] == 'Repo is too large'


def test_repo_size_fail_double():
    max_py_files_count = 1
    path_to_repo = 'test_fixtures{}general_repo'.format(os.path.sep)
    path_to_original_repo = 'test_fixtures{}general_repo_origin'.format(os.path.sep)
    output = are_repos_too_large(path_to_repo, max_py_files_count, path_to_original_repo)
    assert isinstance(output, tuple)
    assert output[0] == 'Repo is too large'


def test_repo_size_ok_single():
    max_py_files_count = 1000
    path_to_repo = 'test_fixtures{}general_repo'.format(os.path.sep)
    output = are_repos_too_large(path_to_repo, max_py_files_count)
    assert output is None


def test_repo_size_ok_double():
    max_py_files_count = 1000
    path_to_repo = 'test_fixtures{}general_repo'.format(os.path.sep)
    path_to_original_repo = 'test_fixtures{}general_repo_origin'.format(os.path.sep)
    output = are_repos_too_large(path_to_repo, max_py_files_count, path_to_original_repo)
    assert output is None
