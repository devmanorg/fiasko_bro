from fiasko_bro import validators
from fiasko_bro.code_validator import CodeValidator


def test_no_local_imports_fail(test_repo):
    expected_output = 'has_local_import', 'no_local_imports_test_file.py'
    whitelists = CodeValidator.whitelists
    output = validators.has_no_local_imports(
        project_folder=test_repo,
        whitelists=whitelists,
    )
    assert output == expected_output


def test_no_local_imports_ok(test_repo):
    whitelists = {'has_no_local_imports': ['no_local_imports_test_file.py']}
    output = validators.has_no_local_imports(
        project_folder=test_repo,
        whitelists=whitelists,
    )
    assert output is None
