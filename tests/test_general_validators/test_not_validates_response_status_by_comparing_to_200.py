from fiasko_bro import validators


def test_not_validates_response_status_by_comparing_to_200(test_repo):
    expected_output = 'compare_response_status_to_200', ''
    output = validators.not_validates_response_status_by_comparing_to_200(
        solution_repo=test_repo,
    )
    assert output == expected_output
