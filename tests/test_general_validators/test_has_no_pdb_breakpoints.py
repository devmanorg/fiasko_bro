from fiasko_bro.validators import has_pdb_breakpoint


def test_has_no_pdb_breakpoint_fails(test_repo):
    expected_output = 'file_with_pdb_breakpoint.py'
    output = has_pdb_breakpoint(test_repo)
    assert output == expected_output


def test_has_no_pdb_breakpoint_succeeds(origin_repo):
    output = has_pdb_breakpoint(origin_repo)
    assert output is None
