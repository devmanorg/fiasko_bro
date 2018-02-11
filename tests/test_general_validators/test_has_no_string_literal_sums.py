from fiasko_bro import validators


def test_has_no_string_literal_sums_fail(test_repo):
    expected_output = 'has_string_sum'
    output = validators.has_no_string_literal_sums(solution_repo=test_repo)
    assert output[0] == expected_output
