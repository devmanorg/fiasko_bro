from fiasko_bro import validators


def test_mccabe_difficulty(test_repo):
    max_complexity = 7
    expected_output = 'function_with_big_complexity'
    output = validators.too_difficult_by_mccabe(
        project_folder=test_repo,
        max_complexity=max_complexity
    )
    assert output == expected_output
