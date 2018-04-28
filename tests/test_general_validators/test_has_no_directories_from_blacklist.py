from fiasko_bro import defaults
from fiasko_bro import validators


def test_has_no_directories_from_blacklist_fails(test_repo):
    expected_output = 'data_in_repo', '.vscode'
    output = validators.has_no_directories_from_blacklist(
        project_folder=test_repo,
        data_directories=defaults.VALIDATION_PARAMETERS['data_directories']
    )
    assert output == expected_output


def test_has_no_directories_from_blacklist_succeeds(origin_repo):
    output = validators.has_no_directories_from_blacklist(
        project_folder=origin_repo,
        data_directories=defaults.VALIDATION_PARAMETERS['data_directories']
    )
    assert output is None
