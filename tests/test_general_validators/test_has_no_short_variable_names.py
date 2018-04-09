from fiasko_bro import defaults
from fiasko_bro import validators


def test_has_no_short_variable_names_fail(test_repo):
    expected_output = 'bad_titles', 'sv'
    minimum_name_length = 3
    output = validators.has_no_short_variable_names(
        project_folder=test_repo,
        whitelists=defaults.WHITELISTS,
        minimum_name_length=minimum_name_length,
    )
    assert output == expected_output


def test_has_no_short_variable_names_ok(test_repo):
    whitelists = {'has_no_short_variable_names': ['sv']}
    minimum_name_length = 3
    output = validators.has_no_short_variable_names(
        project_folder=test_repo,
        whitelists=whitelists,
        minimum_name_length=minimum_name_length,
    )
    assert output is None
