from fiasko_bro import validators


def test_readme_file_exist(test_repo):
    readme_filename = 'changed_readme.md'
    output = validators.has_readme_file(
        solution_repo=test_repo,
        readme_filename=readme_filename,
    )
    assert output is None


def test_readme_file_not_exist(test_repo):
    readme_filename = 'not_exist_readme.md'
    expected_output = 'need_readme', 'нет %s' % readme_filename
    output = validators.has_readme_file(
        solution_repo=test_repo,
        readme_filename=readme_filename,
    )
    assert output == expected_output
