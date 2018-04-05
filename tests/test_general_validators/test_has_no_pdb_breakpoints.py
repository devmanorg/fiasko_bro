from fiasko_bro.validators import has_no_pdb_breakpoints


def test_has_no_pdb_breakpoint_fails(test_repo):
    expected_output = 'has_pdb_breakpoint', 'file_with_pdb_breakpoint.py'
    output = has_no_pdb_breakpoints(test_repo)
    assert output == expected_output


def test_has_no_pdb_breakpoint_succeeds(origin_repo):
    output = has_no_pdb_breakpoints(origin_repo)
    assert output is None
