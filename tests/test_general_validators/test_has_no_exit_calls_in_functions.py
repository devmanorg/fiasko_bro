from fiasko_bro import defaults
from fiasko_bro.validators import has_no_exit_calls_in_functions


def test_has_no_exit_calls_in_functions_fails(test_repo):
    expected_output = 'has_exit_calls_in_function', 'function_with_exit_call'
    output = has_no_exit_calls_in_functions(test_repo, whitelists=defaults.WHITELISTS)
    assert output == expected_output


def test_has_no_exit_calls_in_functions_succeds(origin_repo):
    output = has_no_exit_calls_in_functions(origin_repo, whitelists=defaults.WHITELISTS)
    assert output is None
