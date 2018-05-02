from fiasko_bro.validators import mutable_default_arguments


def test_mutable_default_arguments_fails(test_repo):
    expected_output = 'file_with_mutable_default_arguments.py:3'
    output = mutable_default_arguments(test_repo)
    assert output == expected_output


def test_mutable_default_arguments_succeeds(origin_repo):
    output = mutable_default_arguments(origin_repo)
    assert output is None
