from fiasko_bro import validators
from fiasko_bro.code_validator import CodeValidator


def test_has_variables_from_blacklist_fail(test_repo):
    expected_output = 'bad_titles', 'data'
    whitelists = CodeValidator.whitelists
    blacklists = CodeValidator.blacklists
    output = validators.has_variables_from_blacklist(
        solution_repo=test_repo,
        whitelists=whitelists,
        blacklists=blacklists,
    )
    assert output == expected_output


def test_has_variables_from_blacklist_with_file_in_whitelist_ok(test_repo):
    whitelists = {'has_variables_from_blacklist': [
        'variables_from_blacklist_test_file.py'
    ]}
    blacklists = CodeValidator.blacklists
    output = validators.has_variables_from_blacklist(
        solution_repo=test_repo,
        whitelists=whitelists,
        blacklists=blacklists,
    )
    assert output is None


def test_has_variables_from_blacklist_with_var_in_blacklist_ok(test_repo):
    whitelists = CodeValidator.whitelists
    blacklists_original = CodeValidator.blacklists
    blacklist_for_test = blacklists_original.copy()
    blacklist_for_test['has_variables_from_blacklist'].remove('data')
    output = validators.has_variables_from_blacklist(
        solution_repo=test_repo,
        whitelists=whitelists,
        blacklists=blacklist_for_test,
    )
    assert output is None
