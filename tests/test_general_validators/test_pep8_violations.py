from fiasko_bro import defaults
from fiasko_bro import validators


def test_pep8_violations_fail(test_repo):
    whitelists = defaults.WHITELISTS
    output = validators.is_pep8_fine(
        project_folder=test_repo,
        allowed_max_pep8_violations=0,
        whitelists=whitelists,
        max_pep8_line_length=79,
    )
    assert isinstance(output, tuple)
    assert output[0] == 'pep8'


def test_pep8_violations_ok(test_repo):
    expected_output = None
    whitelists = defaults.WHITELISTS
    output = validators.is_pep8_fine(
        project_folder=test_repo,
        allowed_max_pep8_violations=1000,
        whitelists=whitelists,
        max_pep8_line_length=1000,
    )
    assert output == expected_output
