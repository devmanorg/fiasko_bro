from fiasko_bro import defaults
from fiasko_bro import validators


def test_has_variables_from_blacklist_fail(test_repo):
    expected_output = 'data'
    output = validators.has_variables_from_blacklist(
        project_folder=test_repo,
        bad_variables_paths_to_ignore=defaults.VALIDATION_PARAMETERS['bad_variables_paths_to_ignore'],
        bad_variable_names=defaults.VALIDATION_PARAMETERS['bad_variable_names']
    )
    assert output == expected_output


def test_has_variables_from_blacklist_with_file_in_whitelist_ok(test_repo):
    output = validators.has_variables_from_blacklist(
        project_folder=test_repo,
        bad_variables_paths_to_ignore=['variables_from_blacklist_test_file.py'],
        bad_variable_names=defaults.VALIDATION_PARAMETERS['bad_variable_names']
    )
    assert output is None


def test_has_variables_from_blacklist_with_var_in_blacklist_ok(test_repo):
    bad_variable_names = list(defaults.VALIDATION_PARAMETERS['bad_variable_names'])
    bad_variable_names.remove('data')
    output = validators.has_variables_from_blacklist(
        project_folder=test_repo,
        bad_variables_paths_to_ignore=defaults.VALIDATION_PARAMETERS['bad_variables_paths_to_ignore'],
        bad_variable_names=bad_variable_names
    )
    assert output is None
