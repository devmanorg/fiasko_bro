from fiasko_bro import defaults
from fiasko_bro.pre_validation_checks import file_has_bom


def test_file_has_bom_fail(test_repo_with_bom_path):
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    output = file_has_bom(test_repo_with_bom_path, directories_to_skip)
    assert isinstance(output, str)


def test_file_has_bom_ok(test_repo_without_bom_path):
    directories_to_skip = defaults.VALIDATION_PARAMETERS['directories_to_skip']
    output = file_has_bom(test_repo_without_bom_path, directories_to_skip)
    assert output is None
