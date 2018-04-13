from fiasko_bro import validators
from fiasko_bro import defaults
from fiasko_bro.i18n import _


def test_has_local_var_named_as_global_fail(test_repo):
    expected_output = 'has_locals_named_as_globals', _('for example, %s') % 'LOCAL_VAR'
    output = validators.has_local_var_named_as_global(
        project_folder=test_repo,
        whitelists=defaults.WHITELISTS,
        max_indentation_level=defaults.VALIDATION_PARAMETERS['max_indentation_level']
    )
    assert output == expected_output


def test_has_local_var_named_as_global_ok(test_repo):
    whitelists = {'has_local_var_named_as_global': [
        'local_var_as_global_test_file.py'
    ]}
    max_indentation_level = defaults.VALIDATION_PARAMETERS[
        'max_indentation_level'
    ]
    output = validators.has_local_var_named_as_global(
        project_folder=test_repo,
        whitelists=whitelists,
        max_indentation_level=max_indentation_level,
    )
    assert output is None
