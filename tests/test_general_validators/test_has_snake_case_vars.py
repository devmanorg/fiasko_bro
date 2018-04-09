import copy

from fiasko_bro import defaults
from fiasko_bro import validators


def test_is_snake_case_fail(test_repo):
    output = validators.is_snake_case(
        project_folder=test_repo,
        whitelists=defaults.WHITELISTS,
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
    whitelists = copy.deepcopy(defaults.WHITELISTS)
    whitelists['is_snake_case'].extend(vars_used_not_in_snake_case)
    output = validators.is_snake_case(
        project_folder=test_repo,
        whitelists=whitelists,
    )
    assert output is expected_output
