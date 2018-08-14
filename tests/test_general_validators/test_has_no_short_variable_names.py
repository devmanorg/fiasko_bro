from fiasko_bro import defaults
from fiasko_bro import validators


def test_short_variable_name_fail(test_repo):
    expected_output = 'sv'
    min_variable_name_length = 3
    output = validators.short_variable_name(
        project_folder=test_repo,
        valid_short_variable_names=defaults.VALIDATION_PARAMETERS['valid_short_variable_names'],
        min_variable_name_length=min_variable_name_length,
    )
    assert output == expected_output


def test_short_variable_name_ok(test_repo):
    min_variable_name_length = 3
    output = validators.short_variable_name(
        project_folder=test_repo,
        valid_short_variable_names=['sv'],
        min_variable_name_length=min_variable_name_length,
    )
    assert output is None
