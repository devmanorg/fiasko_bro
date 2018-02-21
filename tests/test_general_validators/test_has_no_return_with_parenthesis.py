from fiasko_bro.validators import has_no_return_with_parenthesis


def test_has_no_return_with_parenthesis_fails(test_repo):
    expected_output = 'return_with_parenthesis', 'file_with_return_with_parenthesis.py:3'
    output = has_no_return_with_parenthesis(test_repo)
    assert output == expected_output


def test_has_no_return_with_parenthesis_succeeds(origin_repo):
    output = has_no_return_with_parenthesis(origin_repo)
    assert output is None
