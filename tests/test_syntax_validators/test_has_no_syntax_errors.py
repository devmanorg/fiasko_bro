from fiasko_bro import validators


def test_has_no_syntax_errors_fail(test_repo):
    output = validators.has_no_syntax_errors(test_repo)
    assert isinstance(output, tuple)
    assert output[0] == 'syntax_error'


def test_has_no_syntax_errors_ok(control_repo):
    output = validators.has_no_syntax_errors(control_repo)
    assert output is None
