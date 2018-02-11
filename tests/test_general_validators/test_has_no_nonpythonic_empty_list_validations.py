from fiasko_bro import validators


def test_has_no_nonpythonic_empty_list_validations(test_repo):
    expected_output = 'nonpythonic_empty_list_validation', ''
    output = validators.has_no_nonpythonic_empty_list_validations(
        solution_repo=test_repo,
    )
    assert output == expected_output
