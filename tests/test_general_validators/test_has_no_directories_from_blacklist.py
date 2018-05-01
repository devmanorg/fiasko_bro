from fiasko_bro import validators


def test_has_no_directories_from_blacklist_fails_simple_data_directory(test_repo):
    expected_output = 'data_in_repo', '.vscode'
    output = validators.has_no_directories_from_blacklist(
        project_folder=test_repo,
        data_directories=['.vscode']
    )
    assert output == expected_output


def test_has_no_directories_from_blacklist_fails_nested_data_directory(test_repo):
    expected_output = 'data_in_repo', '__pycache__'
    output = validators.has_no_directories_from_blacklist(
        project_folder=test_repo,
        data_directories=['__pycache__']
    )
    assert output == expected_output


def test_has_no_directories_from_blacklist_succeeds_directories_not_tracked(origin_repo):
    output = validators.has_no_directories_from_blacklist(
        project_folder=origin_repo,
        data_directories=['.vscode']
    )
    assert output is None


def test_has_no_directories_from_blacklist_succeeds_directories_not_found(test_repo):
    output = validators.has_no_directories_from_blacklist(
        project_folder=test_repo,
        data_directories=['the_name_of_data_dir_01236']
    )
    assert output is None
