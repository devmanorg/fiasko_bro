from fiasko_bro.validators import has_no_return_with_parenthesis
from fiasko_bro.i18n import _


def test_has_no_return_with_parenthesis_fails(test_repo):
    expected_output = 'return_with_parenthesis', _('for example, the line number %s') % 3
    output = has_no_return_with_parenthesis(test_repo)
    assert output == expected_output


def test_has_no_return_with_parenthesis_succeeds(origin_repo):
    output = has_no_return_with_parenthesis(origin_repo)
    assert output is None
