from fiasko_bro import defaults
from fiasko_bro import validators


def test_code_too_nested_fails(test_repo):
    max_indentation_level = defaults.VALIDATION_PARAMETERS[
        'max_indentation_level'
    ]
    deep_nesting_paths_to_ignore = defaults.VALIDATION_PARAMETERS[
        'deep_nesting_paths_to_ignore'
    ]
    output = validators.code_too_nested(
        project_folder=test_repo,
        tab_size=defaults.VALIDATION_PARAMETERS['tab_size'],
        max_indentation_level=max_indentation_level,
        deep_nesting_paths_to_ignore=deep_nesting_paths_to_ignore
    )
    assert isinstance(output, str)
    assert 'complex_functions' in output


def test_code_too_nested_succeeds(origin_repo):
    max_indentation_level = defaults.VALIDATION_PARAMETERS[
        'max_indentation_level'
    ]
    deep_nesting_paths_to_ignore = defaults.VALIDATION_PARAMETERS[
        'deep_nesting_paths_to_ignore'
    ]
    output = validators.code_too_nested(
        project_folder=origin_repo,
        tab_size=defaults.VALIDATION_PARAMETERS['tab_size'],
        max_indentation_level=max_indentation_level,
        deep_nesting_paths_to_ignore=deep_nesting_paths_to_ignore
    )
    assert output is None
