from fiasko_bro.validators import urls_with_hardcoded_get_parameters


def test_urls_with_hardcoded_get_parameters_fails(test_repo):
    expected_output = 'file_with_url_with_hardcoded_query_params.py:2'
    output = urls_with_hardcoded_get_parameters(test_repo)
    assert output == expected_output


def test_urls_with_hardcoded_get_parameters_succeeds(origin_repo):
    output = urls_with_hardcoded_get_parameters(origin_repo)
    assert output is None
