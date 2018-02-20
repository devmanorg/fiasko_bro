from fiasko_bro import validators
from fiasko_bro.code_validator import CodeValidator


def test_is_nesting_too_deep_fails(test_repo):
    max_indentation_level = CodeValidator._default_settings[
        'max_indentation_level'
    ]
    output = validators.is_nesting_too_deep(
        solution_repo=test_repo,
        tab_size=CodeValidator._default_settings['tab_size'],
        max_indentation=max_indentation_level,
        whitelists=CodeValidator.whitelists,
    )
    assert isinstance(output, tuple)
    assert output[0] == 'too_nested'
    assert 'complex_functions' in output[1]


def test_is_nesting_too_deep_succeeds(origin_repo):
    max_indentation_level = CodeValidator._default_settings[
        'max_indentation_level'
    ]
    output = validators.is_nesting_too_deep(
        solution_repo=origin_repo,
        tab_size=CodeValidator._default_settings['tab_size'],
        max_indentation=max_indentation_level,
        whitelists=CodeValidator.whitelists,
    )
    assert output is None
