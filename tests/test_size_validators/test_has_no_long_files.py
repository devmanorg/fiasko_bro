from fiasko_bro import defaults
from fiasko_bro.pre_validation_checks import has_no_long_py_files


def test_has_no_long_py_files_fails(general_repo_path):
    expected_output = 'file_too_long', 'very_long_file.py'
    max_number_of_lines = defaults.VALIDATION_PARAMETERS['max_number_of_lines']
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    output = has_no_long_py_files(
        project_path=general_repo_path,
        max_number_of_lines=max_number_of_lines,
        directories_to_skip=directories_to_skip
    )
    assert output == expected_output


def test_has_no_long_py_files_succeeds(general_repo_origin_path):
    max_number_of_lines = defaults.VALIDATION_PARAMETERS['max_number_of_lines']
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    output = has_no_long_py_files(
        project_path=general_repo_origin_path,
        max_number_of_lines=max_number_of_lines,
        directories_to_skip=directories_to_skip
    )
    assert output is None
