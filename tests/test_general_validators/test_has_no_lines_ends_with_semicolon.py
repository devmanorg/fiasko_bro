from fiasko_bro.validators import has_no_lines_ends_with_semicolon


def test_has_no_lines_ends_with_semicolon_fails(test_repo):
    expected_output = 'has_semicolons', 'file_with_semicolons.py'
    output = has_no_lines_ends_with_semicolon(test_repo)
    assert output == expected_output


def test_has_no_lines_ends_with_semicolon_succeeds(origin_repo):
    output = has_no_lines_ends_with_semicolon(origin_repo)
    assert output is None
