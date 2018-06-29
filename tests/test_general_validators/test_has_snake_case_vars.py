from fiasko_bro import defaults
from fiasko_bro import validators


def test_camel_case_variable_name_fail(test_repo):
    parameters = defaults.VALIDATION_PARAMETERS
    valid_non_snake_case_left_hand_values = parameters['valid_non_snake_case_left_hand_values']
    valid_non_snake_case_right_hand_values = parameters['valid_non_snake_case_right_hand_values']
    output = validators.camel_case_variable_name(
        project_folder=test_repo,
        valid_non_snake_case_left_hand_values=valid_non_snake_case_left_hand_values,
        valid_non_snake_case_right_hand_values=valid_non_snake_case_right_hand_values
    )
    assert isinstance(output, str)


def test_camel_case_variable_name_succeeds_for_extended_left_hand_whitelist(test_repo):
    parameters = defaults.VALIDATION_PARAMETERS
    valid_non_snake_case_left_hand_values = parameters['valid_non_snake_case_left_hand_values']
    valid_non_snake_case_right_hand_values = parameters['valid_non_snake_case_right_hand_values']
    vars_used_not_in_snake_case = {
        'CamelCaseVar',
        'lowerCamelCaseVar',
        'SoMeWieRdCasE'
    }
    left_hand = valid_non_snake_case_left_hand_values.union(vars_used_not_in_snake_case)
    output = validators.camel_case_variable_name(
        project_folder=test_repo,
        valid_non_snake_case_left_hand_values=left_hand,
        valid_non_snake_case_right_hand_values=valid_non_snake_case_right_hand_values
    )
    assert output is None
