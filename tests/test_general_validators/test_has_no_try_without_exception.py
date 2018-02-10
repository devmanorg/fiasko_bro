from fiasko_bro import validators


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


def test_has_no_try_without_exception_no_type_exception(origin_repo):
    expected_output = (
        'broad_except',
        ''
    )
    output = validators.has_no_try_without_exception(
        solution_repo=origin_repo,
    )
    assert output == expected_output
