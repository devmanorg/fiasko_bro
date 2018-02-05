from fiasko_bro import validators


def test_no_star_imports_fail(test_repo):
    expected_output = 'has_star_import', ''
    output = validators.has_no_star_imports(
        solution_repo=test_repo,
    )
    assert output == expected_output
