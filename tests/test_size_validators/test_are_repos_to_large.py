from fiasko_bro.pre_validation_checks import are_repos_too_large


def test_repo_size_fail_single(general_repo):
    max_py_files_count = 1
    output = are_repos_too_large(general_repo, max_py_files_count)
    assert isinstance(output, tuple)
    assert output[0] == 'Repo is too large'


def test_repo_size_fail_double(general_repo, general_repo_origin):
    max_py_files_count = 1
    output = are_repos_too_large(general_repo, max_py_files_count, general_repo_origin)
    assert isinstance(output, tuple)
    assert output[0] == 'Repo is too large'


def test_repo_size_ok_single(general_repo):
    max_py_files_count = 1000
    output = are_repos_too_large(general_repo, max_py_files_count)
    assert output is None


def test_repo_size_ok_double(general_repo, general_repo_origin):
    max_py_files_count = 1000
    output = are_repos_too_large(general_repo, max_py_files_count, general_repo_origin)
    assert output is None
