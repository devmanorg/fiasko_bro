from fiasko_bro import validators
from fiasko_bro import defaults
from fiasko_bro.i18n import _


def test_has_local_var_named_as_global_fail(test_repo):
    expected_output = _('for example, %s') % 'LOCAL_VAR'
    ignore_list = defaults.VALIDATION_PARAMETERS['local_var_named_as_global_paths_to_ignore']
    output = validators.has_local_var_named_as_global(
        project_folder=test_repo,
        local_var_named_as_global_paths_to_ignore=ignore_list,
        max_indentation_level=defaults.VALIDATION_PARAMETERS['max_indentation_level']
    )
    assert output == expected_output


def test_has_local_var_named_as_global_ok(test_repo):
    max_indentation_level = defaults.VALIDATION_PARAMETERS[
        'max_indentation_level'
    ]
    output = validators.has_local_var_named_as_global(
        project_folder=test_repo,
        local_var_named_as_global_paths_to_ignore=['local_var_as_global_test_file.py'],
        max_indentation_level=max_indentation_level,
    )
    assert output is None
