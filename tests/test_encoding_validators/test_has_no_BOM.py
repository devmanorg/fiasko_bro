from fiasko_bro.pre_validation_checks import has_no_bom


def test_has_no_bom_fail(test_repo_with_bom_path):
    output = has_no_bom(test_repo_with_bom_path)
    assert isinstance(output, tuple)
    assert output[0] == 'has_bom'


def test_has_no_bom_ok(test_repo_without_bom_path):
    output = has_no_bom(test_repo_without_bom_path)
    assert output is None
