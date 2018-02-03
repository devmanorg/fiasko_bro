import pytest

from fiasko_bro import validators, LocalRepositoryInfo


def test_are_tabs_used_for_indentation_fail_for_py_file(test_repo):
    excpected_output = 'tabs_used_for_indents', ''
    output = validators.are_tabs_used_for_indentation(
        solution_repo=test_repo,
    )
    assert output == excpected_output


@pytest.mark.skip(reason="No support for frontend files yet")
def test_are_tabs_used_for_indentation_fail_for_js_file(temp_dir_for_tests):
    excpected_output = 'tabs_used_for_indents', ''
    js_file_with_tabs = temp_dir_for_tests.join('js_file_with_tabs.js')
    js_file_with_tabs.write(
        'function showMessage() {\n\talert( "tabs!" );\n}'
    )
    output = validators.are_tabs_used_for_indentation(
        solution_repo=LocalRepositoryInfo(temp_dir_for_tests),
    )
    assert output == excpected_output


@pytest.mark.skip(reason="No support for frontend files yet")
def test_are_tabs_used_for_indentation_fail_for_html_file(temp_dir_for_tests):
    excpected_output = 'tabs_used_for_indents', ''
    html_file_with_tabs_ = temp_dir_for_tests.join('html_with_tabs_file.html')
    html_file_with_tabs_.write(
        '<div>\n\t<span>"tabs!"</span>\n</div>\n'
    )
    output = validators.are_tabs_used_for_indentation(
        solution_repo=LocalRepositoryInfo(temp_dir_for_tests),
    )
    assert output == excpected_output


@pytest.mark.skip(reason="No support for frontend files yet")
def test_are_tabs_used_for_indentation_fail_for_css_file(temp_dir_for_tests):
    excpected_output = 'tabs_used_for_indents', ''
    css_file_with_tabs_ = temp_dir_for_tests.join('html_with_tabs_file.html')
    css_file_with_tabs_.write(
        'h1 {\n\tcolor: navy;\n}'
    )
    output = validators.are_tabs_used_for_indentation(
        solution_repo=LocalRepositoryInfo(temp_dir_for_tests),
    )
    assert output == excpected_output
