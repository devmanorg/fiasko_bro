from fiasko_bro.validators import has_no_exit_calls_in_functions
from fiasko_bro.code_validator import CodeValidator


def test_has_no_exit_calls_in_functions_fails(test_repo):
    expected_output = 'has_exit_calls_in_function', 'function_with_exit_call'
    output = has_no_exit_calls_in_functions(test_repo, whitelists=CodeValidator.whitelists)
    assert output == expected_output


def test_has_no_exit_calls_in_functions_succeds(origin_repo):
    output = has_no_exit_calls_in_functions(origin_repo, whitelists=CodeValidator.whitelists)
    assert output is None
