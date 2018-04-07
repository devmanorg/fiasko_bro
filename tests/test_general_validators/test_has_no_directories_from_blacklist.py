from fiasko_bro import validators
from fiasko_bro.code_validator import CodeValidator


def test_has_no_directories_from_blacklist(test_repo):
    expected_output = 'data_in_repo', '.vscode'
    blacklists = CodeValidator.blacklists
    output = validators.has_no_directories_from_blacklist(
        project_folder=test_repo,
        blacklists=blacklists,
    )
    assert output == expected_output


def test_no_star_imports_ok(origin_repo):
    blacklists = CodeValidator.blacklists
    output = validators.has_no_directories_from_blacklist(
        project_folder=origin_repo,
        blacklists=blacklists,
    )
    assert output is None
