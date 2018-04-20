from fiasko_bro import defaults
from fiasko_bro.validators import long_file


def test_long_file_fails(test_repo):
    expected_output = 'very_long_file.py'
    max_number_of_lines = defaults.VALIDATION_PARAMETERS['max_number_of_lines']
    output = long_file(
        project_folder=test_repo,
        max_number_of_lines=max_number_of_lines
    )
    assert output == expected_output


def test_long_file_succeeds(origin_repo):
    max_number_of_lines = defaults.VALIDATION_PARAMETERS['max_number_of_lines']
    output = long_file(
        project_folder=origin_repo,
        max_number_of_lines=max_number_of_lines
    )
    assert output is None
