from fiasko_bro.validators import has_no_mutable_default_arguments


def test_has_no_mutable_default_arguments_fails(test_repo):
    expected_output = 'mutable_default_arguments', ''
    output = has_no_mutable_default_arguments(test_repo)
    assert output == expected_output


def test_has_no_mutable_default_arguments_succeeds(origin_repo):
    output = has_no_mutable_default_arguments(origin_repo)
    assert output is None
