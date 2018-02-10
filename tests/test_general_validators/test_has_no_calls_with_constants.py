from fiasko_bro import validators
from fiasko_bro.code_validator import CodeValidator


def test_has_no_calls_with_constants_fail(test_repo):
    whitelists = CodeValidator.whitelists
    expected_output = 'magic_numbers', 'например, 5'
    output = validators.has_no_calls_with_constants(
        solution_repo=test_repo,
        whitelists=whitelists,
    )
    assert output == expected_output


def test_has_no_calls_with_constants_ok(origin_repo):
    whitelists = CodeValidator.whitelists
    output = validators.has_no_calls_with_constants(
        solution_repo=origin_repo,
        whitelists=whitelists,
    )
    assert output is None
