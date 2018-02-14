import os.path
from fiasko_bro.pre_validation_checks import are_sources_in_utf


def test_are_sources_in_utf_fail():
    path_to_repo = 'test_fixtures{}encoding_repo'.format(os.path.sep)
    output = are_sources_in_utf(path_to_repo)
    assert isinstance(output, tuple)
    assert output[0] == 'sources_not_utf_8'


def test_are_sources_in_utf_ok():
    path_to_repo = 'test_fixtures{}general_repo'.format(os.path.sep)
    output = are_sources_in_utf(path_to_repo)
    assert output is None
