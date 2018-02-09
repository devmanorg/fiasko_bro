from fiasko_bro import validators
from fiasko_bro.code_validator import CodeValidator


def test_pep8_violations_fail(test_repo):
    expected_output = 'pep8', '31 нарушений'
    whitelists = CodeValidator.whitelists
    output = validators.is_pep8_fine(
        solution_repo=test_repo,
        allowed_max_pep8_violations=0,
        whitelists=whitelists,
        max_pep8_line_length=79,
    )
    assert isinstance(expected_output, tuple)
    assert expected_output[0] == 'pep8'


def test_pep8_violations_ok(test_repo):
    expected_output = None
    whitelists = CodeValidator.whitelists
    output = validators.is_pep8_fine(
        solution_repo=test_repo,
        allowed_max_pep8_violations=1000,
        whitelists=whitelists,
        max_pep8_line_length=1000,
    )
    assert output == expected_output
