from fiasko_bro.validators import slice_starts_from_zero


def test_slice_starts_from_zero_fails(test_repo):
    expected_output = 'file_with_slices_starting_with_zero.py'
    output = slice_starts_from_zero(test_repo)
    assert output == expected_output


def test_slice_starts_from_zero_succeeds(origin_repo):
    output = slice_starts_from_zero(origin_repo)
    assert output is None

