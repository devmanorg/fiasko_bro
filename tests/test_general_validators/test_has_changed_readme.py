from fiasko_bro import validators


def test_readme_changed_succeeds(test_repo, origin_repo):
    output = validators.readme_not_changed(
        project_folder=test_repo,
        readme_filename='changed_readme.md',
        original_project_folder=origin_repo,
    )
    assert output is None


def test_readme_changed_fails(test_repo, origin_repo):
    expected_output = ''
    output = validators.readme_not_changed(
        project_folder=test_repo,
        readme_filename='unchanged_readme.md',
        original_project_folder=origin_repo,
    )
    assert output == expected_output
