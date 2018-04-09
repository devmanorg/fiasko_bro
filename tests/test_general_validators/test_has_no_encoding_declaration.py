from fiasko_bro import defaults
from fiasko_bro.validators import has_no_encoding_declaration


def test_has_no_encoding_declarations_fails(origin_repo):
    expected_output = 'has_encoding_declarations', 'file_with_encoding_declarations.py'
    output = has_no_encoding_declaration(
        project_folder=origin_repo,
        whitelists=defaults.WHITELISTS
    )
    assert output == expected_output


def test_has_no_encoding_declarations_succeeds(test_repo):
    output = has_no_encoding_declaration(
        project_folder=test_repo,
        whitelists=defaults.WHITELISTS
    )
    assert output is None

