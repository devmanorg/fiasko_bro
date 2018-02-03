from fiasko_bro import validators, LocalRepositoryInfo


def test_has_no_try_without_exception_fail(test_repo):
    expected_output = (
        'broad_except',
        'Exception – слишком широкий тип исключений;'
        ' укажи подробнее, какую ошибку ты ловишь'
    )
    output = validators.has_no_try_without_exception(
        solution_repo=test_repo,
    )
    assert output == expected_output


def test_has_no_try_without_exception_short_fail(temp_dir_for_tests):
    expected_output = (
        'broad_except', ''
    )
    no_except_spec_file = temp_dir_for_tests.join('no_except_spec_file.py')
    no_except_spec_file.write(
        'try:\n    except_var = 0/0\nexcept:\n    return None'
    )
    output = validators.has_no_try_without_exception(
        solution_repo=LocalRepositoryInfo(temp_dir_for_tests),
    )
    assert output == expected_output
