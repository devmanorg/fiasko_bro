from fiasko_bro.validators import has_no_long_files
from fiasko_bro.code_validator import CodeValidator


def test_has_no_long_files_fails(test_repo):
    expected_output = 'file_too_long', 'very_long_file.py'
    max_number_of_lines = CodeValidator._default_settings['max_number_of_lines']
    output = has_no_long_files(
        project_folder=test_repo,
        max_number_of_lines=max_number_of_lines
    )
    assert output == expected_output


def test_has_no_long_files_succeeds(origin_repo):
    max_number_of_lines = CodeValidator._default_settings['max_number_of_lines']
    output = has_no_long_files(
        project_folder=origin_repo,
        max_number_of_lines=max_number_of_lines
    )
    assert output is None
