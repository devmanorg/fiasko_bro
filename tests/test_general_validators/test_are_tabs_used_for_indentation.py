from fiasko_bro import validators
from fiasko_bro import defaults


def test_are_tabs_used_for_indentation_fail_for_py_file(test_repo):
    expected_output = 'tabs_used_for_indents', 'css_with_tabs.css'
    output = validators.are_tabs_used_for_indentation(
        project_folder=test_repo,
        directories_to_skip=defaults.VALIDATION_PARAMETERS['directories_to_skip']
    )
    assert output == expected_output
