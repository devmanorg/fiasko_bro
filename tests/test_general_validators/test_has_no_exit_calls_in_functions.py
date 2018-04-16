from fiasko_bro import defaults
from fiasko_bro.validators import has_no_exit_calls_in_functions


def test_has_no_exit_calls_in_functions_fails(test_repo):
    expected_output = 'has_exit_calls_in_function', 'function_with_exit_call'
    functions_allowed_to_have_exit_calls = defaults.VALIDATION_PARAMETERS[
        'functions_allowed_to_have_exit_calls'
    ]
    output = has_no_exit_calls_in_functions(
        test_repo,
        functions_allowed_to_have_exit_calls=functions_allowed_to_have_exit_calls
    )
    assert output == expected_output


def test_has_no_exit_calls_in_functions_succeds(origin_repo):
    functions_allowed_to_have_exit_calls = defaults.VALIDATION_PARAMETERS[
        'functions_allowed_to_have_exit_calls'
    ]
    output = has_no_exit_calls_in_functions(
        origin_repo,
        functions_allowed_to_have_exit_calls=functions_allowed_to_have_exit_calls
    )
    assert output is None
