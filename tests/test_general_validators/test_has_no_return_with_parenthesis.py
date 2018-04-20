from fiasko_bro.validators import return_with_parenthesis


def test_return_with_parenthesis_fails(test_repo):
    expected_output = 'file_with_return_with_parenthesis.py:3'
    output = return_with_parenthesis(test_repo)
    assert output == expected_output


def test_return_with_parenthesis_succeeds(origin_repo):
    output = return_with_parenthesis(origin_repo)
    assert output is None
