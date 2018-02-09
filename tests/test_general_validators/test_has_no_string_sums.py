from fiasko_bro import validators


def test_has_no_string_sums_fail(test_repo):
    expected_output = 'has_string_sum', ''
    output = validators.has_no_string_sums(solution_repo=test_repo)
    assert output == expected_output
