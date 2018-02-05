from fiasko_bro.code_helpers import is_repo_too_large


def test_repo_size_fail():
    max_py_files_count = 2
    path_to_repo = 'test_fixtures/general_repo'
    expected_output = True
    output = is_repo_too_large(path_to_repo, max_py_files_count)

    assert output == expected_output


def test_repo_size_ok():
    max_py_files_count = 10000
    path_to_repo = 'test_fixtures/general_repo'
    expected_output = None
    output = is_repo_too_large(path_to_repo, max_py_files_count)

    assert output == expected_output
