from fiasko_bro.validators import has_no_extra_dockstrings
from fiasko_bro.code_validator import CodeValidator


def test_has_no_extra_docstrings_fail(test_repo):
    expected_output = 'extra_comments', ''
    output = has_no_extra_dockstrings(
        solution_repo=test_repo,
        whitelists=CodeValidator.whitelists,
        functions_with_docstrings_percent_limit=40,
    )
    assert output == expected_output


def test_has_no_extra_docstrings_succeed(test_repo):
    whitelists = CodeValidator.whitelists
    whitelists['has_no_extra_dockstrings_whitelist'] += ['file_with_too_many_docstrings.py']
    output = has_no_extra_dockstrings(
        solution_repo=test_repo,
        whitelists=whitelists,
        functions_with_docstrings_percent_limit=40,
    )
    assert output is None
