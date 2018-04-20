from fiasko_bro.validators import line_ends_with_semicolon


def test_line_ends_with_semicolon_fails(test_repo):
    expected_output = 'file_with_semicolons.py'
    output = line_ends_with_semicolon(test_repo)
    assert output == expected_output


def test_line_ends_with_semicolon_succeeds(origin_repo):
    output = line_ends_with_semicolon(origin_repo)
    assert output is None
