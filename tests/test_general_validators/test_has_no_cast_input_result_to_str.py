from fiasko_bro.validators import has_no_cast_input_result_to_str


def test_has_no_cast_input_result_to_str_fails(test_repo):
    expected_output = 'str_conversion_of_input_result', 'file_with_input_to_str_cast.py:1'
    output = has_no_cast_input_result_to_str(test_repo)
    assert output == expected_output


def test_has_no_cast_input_result_to_str_succeeds(origin_repo):
    output = has_no_cast_input_result_to_str(origin_repo)
    assert output is None
