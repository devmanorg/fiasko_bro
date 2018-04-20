from fiasko_bro import defaults
from fiasko_bro import validators


def test_data_in_repo(test_repo):
    expected_output = '.vscode'
    output = validators.data_in_repo(
        project_folder=test_repo,
        data_directories=defaults.VALIDATION_PARAMETERS['data_directories']
    )
    assert output == expected_output


def test_no_star_imports_ok(origin_repo):
    output = validators.data_in_repo(
        project_folder=origin_repo,
        data_directories=defaults.VALIDATION_PARAMETERS['data_directories']
    )
    assert output is None
