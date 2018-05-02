from fiasko_bro import validators


def test_data_in_repo_fails_simple_data_directory(test_repo):
    expected_output = '.vscode'
    output = validators.data_in_repo(
        project_folder=test_repo,
        data_directories=['.vscode']
    )
    assert output == expected_output


def test_data_in_repo_fails_nested_data_directory(test_repo):
    expected_output = '__pycache__'
    output = validators.data_in_repo(
        project_folder=test_repo,
        data_directories=['__pycache__']
    )
    assert output == expected_output


def test_data_in_repo_succeeds_directories_not_tracked(origin_repo):
    output = validators.data_in_repo(
        project_folder=origin_repo,
        data_directories=['.vscode']
    )
    assert output is None


def test_data_in_repo_succeeds_directories_not_found(test_repo):
    output = validators.data_in_repo(
        project_folder=test_repo,
        data_directories=['the_name_of_data_dir_01236']
    )
    assert output is None
