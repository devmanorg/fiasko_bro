from fiasko_bro import validators


def test_has_frozen_requirements_no_frozen(test_repo):
    expected_output = 'indent_not_four_spaces', 'for example, line number 4'
    output = validators.has_indents_of_spaces(
        solution_repo=test_repo,
        tab_size=4,
    )
    assert output == expected_output
