from fiasko_bro import validators


def test_nonpythonic_empty_list_validation(test_repo):
    expected_output = 'has_no_nonpythonic_empty_list_validations.py:2'
    output = validators.nonpythonic_empty_list_validation(
        project_folder=test_repo,
    )
    assert output == expected_output
