import copy

from fiasko_bro import defaults
from fiasko_bro import validators


def test_has_variables_from_blacklist_fail(test_repo):
    expected_output = 'bad_titles', 'data'
    output = validators.has_variables_from_blacklist(
        project_folder=test_repo,
        whitelists=defaults.WHITELISTS,
        blacklists=defaults.BLACKLISTS,
    )
    assert output == expected_output


def test_has_variables_from_blacklist_with_file_in_whitelist_ok(test_repo):
    whitelists = {'has_variables_from_blacklist': [
        'variables_from_blacklist_test_file.py'
    ]}
    output = validators.has_variables_from_blacklist(
        project_folder=test_repo,
        whitelists=whitelists,
        blacklists=defaults.BLACKLISTS,
    )
    assert output is None


def test_has_variables_from_blacklist_with_var_in_blacklist_ok(test_repo):
    blacklists = copy.deepcopy(defaults.BLACKLISTS)
    blacklists['has_variables_from_blacklist'].remove('data')
    output = validators.has_variables_from_blacklist(
        project_folder=test_repo,
        whitelists=defaults.WHITELISTS,
        blacklists=blacklists,
    )
    assert output is None
