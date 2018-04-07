from fiasko_bro import validators
from fiasko_bro.code_validator import CodeValidator


def test_is_snake_case_fail(test_repo):
    whitelists = CodeValidator.whitelists
    output = validators.is_snake_case(
        project_folder=test_repo,
        whitelists=whitelists,
    )
    assert isinstance(output, tuple)
    assert output[0] == 'camel_case_vars'


def test_is_snake_case_ok(test_repo):
    expected_output = None
    vars_used_not_in_snake_case = [
        'CamelCaseVar',
        'lowerCamelCaseVar',
        'SoMeWieRdCasE'
    ]
    whitelists = CodeValidator.whitelists
    whitelists['is_snake_case'].extend(vars_used_not_in_snake_case)
    output = validators.is_snake_case(
        project_folder=test_repo,
        whitelists=whitelists,
    )
    assert output is expected_output
