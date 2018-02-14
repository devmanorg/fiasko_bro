from fiasko_bro.validators import has_no_urls_with_hardcoded_arguments


def test_has_no_urls_with_hardcoded_arguments_fails(test_repo):
    expected_output = 'hardcoded_get_params', ''
    output = has_no_urls_with_hardcoded_arguments(test_repo)
    assert output == expected_output


def test_has_no_urls_with_hardcoded_arguments_succeeds(origin_repo):
    output = has_no_urls_with_hardcoded_arguments(origin_repo)
    assert output is None
