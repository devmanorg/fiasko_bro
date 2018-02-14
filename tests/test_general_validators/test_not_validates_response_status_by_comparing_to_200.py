from fiasko_bro import validators


def test_not_validates_response_status_by_comparing_to_200_fails(test_repo):
    expected_output = 'compare_response_status_to_200', ''
    output = validators.not_validates_response_status_by_comparing_to_200(
        solution_repo=test_repo,
    )
    assert output == expected_output


def test_not_validates_response_status_by_comparing_to_200_succeeds(origin_repo):
    output = validators.not_validates_response_status_by_comparing_to_200(
        solution_repo=origin_repo,
    )
    assert output is None
