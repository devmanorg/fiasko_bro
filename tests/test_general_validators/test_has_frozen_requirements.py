from fiasko_bro import validators
from fiasko_bro.i18n import _


def test_has_frozen_requirements_no_frozen(test_repo):
    expected_output = 'unfrozen_requirements', _('for example, %s') % 'django'
    output = validators.has_frozen_requirements(
        project_folder=test_repo,
    )
    assert output == expected_output


def test_has_frozen_requirements_no_requirements_file(origin_repo):
    output = validators.has_frozen_requirements(
        project_folder=origin_repo,
    )
    assert output is None
