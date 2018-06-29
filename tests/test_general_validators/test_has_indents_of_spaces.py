from fiasko_bro import validators


def test_indent_not_multiple_of_tab_size_fails(test_repo):
    expected_output = 'has_indents_of_spaces.py:5'
    output = validators.indent_not_multiple_of_tab_size(
        project_folder=test_repo,
        tab_size=4,
    )
    assert output == expected_output
