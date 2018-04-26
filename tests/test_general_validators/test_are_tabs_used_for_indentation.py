from fiasko_bro import validators


def test_are_tabs_used_for_indentation_fail_for_py_file(test_repo):
    expected_output = 'tabs_used_for_indents', 'js_with_tabs.js'
    output = validators.are_tabs_used_for_indentation(
        solution_repo=test_repo,
    )
    assert output == expected_output
