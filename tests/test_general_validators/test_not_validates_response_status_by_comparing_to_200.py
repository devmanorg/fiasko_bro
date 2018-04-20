from fiasko_bro import validators


def test_validates_response_status_by_comparing_to_200_fails(test_repo):
    expected_output = 'not_validates_response_status_by_comparing_to_200.py:3'
    output = validators.validates_response_status_by_comparing_to_200(
        project_folder=test_repo,
    )
    assert output == expected_output


def test_validates_response_status_by_comparing_to_200_succeeds(origin_repo):
    output = validators.validates_response_status_by_comparing_to_200(
        project_folder=origin_repo,
    )
    assert output is None
