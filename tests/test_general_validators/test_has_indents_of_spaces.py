from fiasko_bro import validators


def test_has_indent_of_four_spaces(test_repo):
    expected_output = 'indent_not_four_spaces', 'has_indents_of_spaces.py:5'
    output = validators.has_indents_of_spaces(
        solution_repo=test_repo,
        tab_size=4,
    )
    assert output == expected_output
