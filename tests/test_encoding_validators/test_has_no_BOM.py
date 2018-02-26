from fiasko_bro.validators import has_no_bom


def test_has_no_bom_fail(test_repo_with_bom):
    output = has_no_bom(test_repo_with_bom)
    assert isinstance(output, tuple)
    assert output[0] == 'has_bom'


def test_has_no_bom_ok(test_repo_without_bom):
    output = has_no_bom(test_repo_without_bom)
    assert output is None
