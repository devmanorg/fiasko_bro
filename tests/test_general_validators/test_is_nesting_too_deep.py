from fiasko_bro import defaults
from fiasko_bro import validators


def test_is_nesting_too_deep_fails(test_repo):
    max_indentation_level = defaults.VALIDATOR_SETTINGS[
        'max_indentation_level'
    ]
    output = validators.is_nesting_too_deep(
        project_folder=test_repo,
        tab_size=defaults.VALIDATOR_SETTINGS['tab_size'],
        max_indentation_level=max_indentation_level,
        whitelists=defaults.WHITELISTS,
    )
    assert isinstance(output, tuple)
    assert output[0] == 'too_nested'
    assert 'complex_functions' in output[1]


def test_is_nesting_too_deep_succeeds(origin_repo):
    max_indentation_level = defaults.VALIDATOR_SETTINGS[
        'max_indentation_level'
    ]
    output = validators.is_nesting_too_deep(
        project_folder=origin_repo,
        tab_size=defaults.VALIDATOR_SETTINGS['tab_size'],
        max_indentation_level=max_indentation_level,
        whitelists=defaults.WHITELISTS,
    )
    assert output is None
