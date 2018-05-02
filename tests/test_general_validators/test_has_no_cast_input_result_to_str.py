from fiasko_bro.validators import casts_input_result_to_str


def test_casts_input_result_to_str_fails(test_repo):
    expected_output = 'file_with_input_to_str_cast.py:1'
    output = casts_input_result_to_str(test_repo)
    assert output == expected_output


def test_casts_input_result_to_str_succeeds(origin_repo):
    output = casts_input_result_to_str(origin_repo)
    assert output is None
