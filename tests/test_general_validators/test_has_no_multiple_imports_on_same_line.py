from fiasko_bro.validators import has_multiple_imports_on_same_line


def test_has_no_multiple_imports_on_same_line_fails(test_repo):
    expected_output = 'file_with_multiple_imports_on_same_line.py:3'
    output = has_multiple_imports_on_same_line(test_repo)
    assert output == expected_output


def test_has_no_mutable_default_arguments_succeeds(origin_repo):
    output = has_multiple_imports_on_same_line(origin_repo)
    assert output is None
