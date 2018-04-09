from fiasko_bro import defaults
from fiasko_bro import validators


def test_no_local_imports_fail(test_repo):
    expected_output = 'has_local_import', 'no_local_imports_test_file.py'
    output = validators.has_no_local_imports(
        project_folder=test_repo,
        whitelists=defaults.WHITELISTS,
    )
    assert output == expected_output


def test_no_local_imports_ok(test_repo):
    whitelists = {'has_no_local_imports': ['no_local_imports_test_file.py']}
    output = validators.has_no_local_imports(
        project_folder=test_repo,
        whitelists=whitelists,
    )
    assert output is None
