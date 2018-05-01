from fiasko_bro import defaults
from fiasko_bro import validators


def test_no_local_imports_fail(test_repo):
    expected_output = 'has_local_import', 'no_local_imports_test_file.py'
    output = validators.has_no_local_imports(
        project_folder=test_repo,
        local_imports_paths_to_ignore=defaults.VALIDATION_PARAMETERS['local_imports_paths_to_ignore']
    )
    assert output == expected_output


def test_no_local_imports_ok(test_repo):
    output = validators.has_no_local_imports(
        project_folder=test_repo,
        local_imports_paths_to_ignore=['no_local_imports_test_file.py']
    )
    assert output is None
