from fiasko_bro.pre_validation_checks import are_sources_in_utf


def test_are_sources_in_utf_fail(encoding_repo_path):
    output = are_sources_in_utf(encoding_repo_path)
    assert isinstance(output, tuple)
    assert output[0] == 'sources_not_utf_8'


def test_are_sources_in_utf_ok(general_repo_path):
    output = are_sources_in_utf(general_repo_path)
    assert output is None
