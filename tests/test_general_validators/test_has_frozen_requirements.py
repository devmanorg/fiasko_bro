from fiasko_bro import validators
from fiasko_bro.i18n import _


def test_requirements_not_frozen_no_frozen(test_repo):
    expected_output = _('for example, %s') % 'django'
    output = validators.requirements_not_frozen(
        project_folder=test_repo,
    )
    assert output == expected_output


def test_requirements_not_frozen_no_requirements_file(origin_repo):
    output = validators.requirements_not_frozen(
        project_folder=origin_repo,
    )
    assert output is None
