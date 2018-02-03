from fiasko_bro import validators
from fiasko_bro.code_validator import CodeValidator


def test_has_no_short_variable_names_fail(test_repo):
    expected_output = 'bad_titles', 'sv'
    whitelists = CodeValidator.whitelists
    minimum_name_length = 3
    output = validators.has_no_short_variable_names(
        solution_repo=test_repo,
        whitelists=whitelists,
        minimum_name_length=minimum_name_length,
    )
    assert output == expected_output


def test_has_no_short_variable_names_ok(test_repo):
    whitelists = {'has_no_short_variable_names': ['sv']}
    minimum_name_length = 3
    output = validators.has_no_short_variable_names(
        solution_repo=test_repo,
        whitelists=whitelists,
        minimum_name_length=minimum_name_length,
    )
    assert output is None
