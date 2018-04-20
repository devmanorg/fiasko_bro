from fiasko_bro.validators import range_starting_from_zero


def test_range_starting_from_zero_fails(test_repo):
    expected_output = 'file_with_range_from_zero.py:4'
    output = range_starting_from_zero(test_repo)
    assert output == expected_output


def test_range_starting_from_zero_succeeds(origin_repo):
    output = range_starting_from_zero(origin_repo)
    assert output is None
