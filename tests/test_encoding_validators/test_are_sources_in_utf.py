from fiasko_bro import defaults
from fiasko_bro.pre_validation_checks import file_not_in_utf8


def test_file_not_in_utf8_fail(encoding_repo_path):
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    output = file_not_in_utf8(encoding_repo_path, directories_to_skip)
    assert isinstance(output, str)


def test_file_not_in_utf8_ok(general_repo_path):
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    output = file_not_in_utf8(general_repo_path, directories_to_skip)
    assert output is None


def test_file_not_in_utf8_uses_whitelist(encoding_repo_path):
    directories_to_skip = ['win1251']
    output = file_not_in_utf8(encoding_repo_path, directories_to_skip)
    assert output is None
