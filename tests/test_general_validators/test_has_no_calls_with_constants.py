from fiasko_bro import defaults
from fiasko_bro import validators


def test_call_with_constants_fail(test_repo):
    expected_output = 'has_no_vars_with_lambda_test_file.py:9'
    output = validators.call_with_constants(
        project_folder=test_repo,
        valid_calls_with_constants=defaults.VALIDATION_PARAMETERS['valid_calls_with_constants']
    )
    assert output == expected_output


def test_call_with_constants_ok(origin_repo):
    output = validators.call_with_constants(
        project_folder=origin_repo,
        valid_calls_with_constants=defaults.VALIDATION_PARAMETERS['valid_calls_with_constants']
    )
    assert output is None
