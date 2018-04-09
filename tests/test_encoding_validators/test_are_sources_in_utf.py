from fiasko_bro import defaults
from fiasko_bro.pre_validation_checks import are_sources_in_utf


def test_are_sources_in_utf_fail(encoding_repo_path):
    directories_to_skip = defaults.VALIDATOR_SETTINGS['directories_to_skip']
    output = are_sources_in_utf(encoding_repo_path, directories_to_skip)
    assert isinstance(output, tuple)
    assert output[0] == 'sources_not_utf_8'


def test_are_sources_in_utf_ok(general_repo_path):
    directories_to_skip = defaults.VALIDATOR_SETTINGS['directories_to_skip']
    output = are_sources_in_utf(general_repo_path, directories_to_skip)
    assert output is None


def test_are_sources_in_utf_uses_whitelist(encoding_repo_path):
    directories_to_skip = ['win1251']
    output = are_sources_in_utf(encoding_repo_path, directories_to_skip)
    assert output is None
