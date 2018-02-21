from fiasko_bro.validators import has_no_slices_starts_from_zero


def test_has_no_slices_starts_from_zero_fails(test_repo):
    expected_output = 'slice_starts_from_zero', 'file_with_slices_starting_with_zero.py'
    output = has_no_slices_starts_from_zero(test_repo)
    assert output == expected_output


def test_has_no_slices_starts_from_zero_succeeds(origin_repo):
    output = has_no_slices_starts_from_zero(origin_repo)
    assert output is None

