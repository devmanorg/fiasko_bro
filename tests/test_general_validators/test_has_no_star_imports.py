from fiasko_bro import validators


def test_no_star_imports_fail(test_repo):
    expected_output = 'no_star_import_test_file.py'
    output = validators.star_import(
        project_folder=test_repo,
    )
    assert output == expected_output
