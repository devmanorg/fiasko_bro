from fiasko_bro import validators
from fiasko_bro.code_validator import CodeValidator


def test_has_local_var_named_as_global_fail(test_repo):
    expected_output = 'has_locals_named_as_globals', 'например, LOCAL_VAR'
    whitelists = CodeValidator.whitelists
    output = validators.has_local_var_named_as_global(
        solution_repo=test_repo,
        whitelists=whitelists,
    )
    assert output == expected_output


def test_has_local_var_named_as_global_ok(test_repo):
    whitelists = {'has_local_var_named_as_global': [
        'local_var_as_global_test_file.py'
    ]}
    output = validators.has_local_var_named_as_global(
        solution_repo=test_repo,
        whitelists=whitelists,
    )
    assert output is None
