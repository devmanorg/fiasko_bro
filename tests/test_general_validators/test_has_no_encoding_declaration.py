from fiasko_bro.validators import has_no_encoding_declaration
from fiasko_bro.code_validator import CodeValidator


def test_has_no_encoding_declarations_fails(origin_repo):
    expected_output = 'has_encoding_declarations', ''
    output = has_no_encoding_declaration(
        solution_repo=origin_repo,
        whitelists=CodeValidator.whitelists
    )
    assert output == expected_output


def test_has_no_encoding_declarations_succeeds(test_repo):
    output = has_no_encoding_declaration(
        solution_repo=test_repo,
        whitelists=CodeValidator.whitelists
    )
    assert output is None

