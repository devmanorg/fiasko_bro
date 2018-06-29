from fiasko_bro import validators
from fiasko_bro.i18n import _


def test_except_block_class_too_broad_fail(test_repo):
    expected_output = _('%s class is too broad; use a more specific exception type') % 'Exception'
    output = validators.except_block_class_too_broad(
        project_folder=test_repo,
    )
    assert output == expected_output


def test_except_block_class_too_broad_no_type_exception(origin_repo):
    expected_output = ''
    output = validators.except_block_class_too_broad(
        project_folder=origin_repo,
    )
    assert output == expected_output
