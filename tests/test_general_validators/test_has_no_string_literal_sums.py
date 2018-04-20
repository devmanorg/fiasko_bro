from fiasko_bro import validators


def test_string_literal_sum_fail(test_repo):
    output = validators.string_literal_sum(project_folder=test_repo)
    assert isinstance(output, str)
