from fiasko_bro import validators


def test_has_no_vars_with_lambda_fail(test_repo):
    expected_output = 'named_lambda', 'has_no_vars_with_lambda_test_file.py:4'
    output = validators.has_no_vars_with_lambda(
        solution_repo=test_repo,
    )
    assert output == expected_output


def test_has_no_vars_with_lambda_ok(origin_repo):
    output = validators.has_no_vars_with_lambda(
        solution_repo=origin_repo,
    )
    assert output is None
