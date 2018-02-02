from fiasko_bro import validators


def test_mccabe_difficulty(test_repo):
    max_complexity = 7
    expected_output = 'mccabe_failure', 'function_for_test_mccabe_fail'
    output = validators.is_mccabe_difficulty_ok(test_repo, max_complexity)
    assert output == expected_output
