from fiasko_bro import validators


def test_variable_assignment_with_lambda_fail(test_repo):
    expected_output = 'has_no_vars_with_lambda_test_file.py:4'
    output = validators.variable_assignment_with_lambda(
        project_folder=test_repo,
    )
    assert output == expected_output


def test_variable_assignment_with_lambda_ok(origin_repo):
    output = validators.variable_assignment_with_lambda(
        project_folder=origin_repo,
    )
    assert output is None
