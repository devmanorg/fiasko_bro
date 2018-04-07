from fiasko_bro import validators


def test_no_star_imports_fail(test_repo):
    expected_output = 'has_star_import', 'no_star_import_test_file.py'
    output = validators.has_no_star_imports(
        project_folder=test_repo,
    )
    assert output == expected_output
