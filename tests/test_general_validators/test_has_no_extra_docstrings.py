from fiasko_bro import defaults
from fiasko_bro.validators import extra_docstrings


def test_has_no_extra_docstrings_fail(test_repo):
    expected_output = 'file_with_too_many_docstrings.py'
    ignore_list = defaults.VALIDATION_PARAMETERS['extra_dockstrings_paths_to_ignore']
    output = extra_docstrings(
        project_folder=test_repo,
        extra_dockstrings_paths_to_ignore=ignore_list,
        functions_with_docstrings_percent_limit=40,
    )
    assert output == expected_output


def test_has_no_extra_docstrings_succeed(test_repo):
    ignore_list = list(defaults.VALIDATION_PARAMETERS['extra_dockstrings_paths_to_ignore'])
    ignore_list += ['file_with_too_many_docstrings.py']
    output = extra_docstrings(
        project_folder=test_repo,
        extra_dockstrings_paths_to_ignore=ignore_list,
        functions_with_docstrings_percent_limit=40,
    )
    assert output is None
