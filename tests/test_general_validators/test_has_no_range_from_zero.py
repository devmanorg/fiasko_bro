from fiasko_bro.validators import has_no_range_from_zero


def test_has_no_range_from_zero_fails(test_repo):
    expected_output = 'manual_zero_in_range', 'file_with_range_from_zero.py:4'
    output = has_no_range_from_zero(test_repo)
    assert output == expected_output


def test_has_no_range_from_zero_succeeds(origin_repo):
    output = has_no_range_from_zero(origin_repo)
    assert output is None
