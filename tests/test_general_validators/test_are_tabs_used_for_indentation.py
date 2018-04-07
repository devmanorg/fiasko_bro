from fiasko_bro import validators


def test_are_tabs_used_for_indentation_fail_for_py_file(test_repo):
    expected_output = 'tabs_used_for_indents', 'css_with_tabs.css'
    output = validators.are_tabs_used_for_indentation(
        project_folder=test_repo,
    )
    assert output == expected_output
