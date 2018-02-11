from fiasko_bro import validators
from fiasko_bro.i18n import _


def test_has_no_try_without_exception_fail(test_repo):
    expected_output = (
        'broad_except',
        _('%s class is too broad; use a more specific exception type') % 'Exception'
    )
    output = validators.has_no_try_without_exception(
        solution_repo=test_repo,
    )
    assert output == expected_output


def test_has_no_try_without_exception_no_type_exception(origin_repo):
    expected_output = (
        'broad_except',
        ''
    )
    output = validators.has_no_try_without_exception(
        solution_repo=origin_repo,
    )
    assert output == expected_output
