from fiasko_bro import defaults
from fiasko_bro.validators import exit_call_in_function


def test_exit_call_in_function_fails(test_repo):
    expected_output = 'function_with_exit_call'
    functions_allowed_to_have_exit_calls = defaults.VALIDATION_PARAMETERS[
        'functions_allowed_to_have_exit_calls'
    ]
    output = exit_call_in_function(
        test_repo,
        functions_allowed_to_have_exit_calls=functions_allowed_to_have_exit_calls
    )
    assert output == expected_output


def test_exit_call_in_function_succeds(origin_repo):
    functions_allowed_to_have_exit_calls = defaults.VALIDATION_PARAMETERS[
        'functions_allowed_to_have_exit_calls'
    ]
    output = exit_call_in_function(
        origin_repo,
        functions_allowed_to_have_exit_calls=functions_allowed_to_have_exit_calls
    )
    assert output is None
