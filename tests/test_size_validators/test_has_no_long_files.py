from fiasko_bro import defaults
from fiasko_bro.pre_validation_checks import file_too_long


def test_file_too_long_fails(general_repo_path):
    expected_output = 'very_long_file.py'
    max_number_of_lines = defaults.VALIDATION_PARAMETERS['max_number_of_lines']
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    output = file_too_long(
        project_path=general_repo_path,
        max_number_of_lines=max_number_of_lines,
        directories_to_skip=directories_to_skip
    )
    assert output == expected_output


def test_file_too_long_succeeds(general_repo_origin_path):
    max_number_of_lines = defaults.VALIDATION_PARAMETERS['max_number_of_lines']
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    output = file_too_long(
        project_path=general_repo_origin_path,
        max_number_of_lines=max_number_of_lines,
        directories_to_skip=directories_to_skip
    )
    assert output is None
