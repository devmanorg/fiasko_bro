from fiasko_bro import get_error_slugs
from fiasko_bro.validators import syntax_error


def test_get_error_slugs_returns_correct_default_pre_validators_and_custom_error_groups():
    expected_output = {
        'file_too_long',
        'file_not_in_utf8',
        'repo_is_too_large',
        'file_has_bom',
        'syntax_error'
    }
    error_groups = {
        'syntax': (syntax_error,),
    }
    output = get_error_slugs(error_validator_groups=error_groups)
    assert output == expected_output
