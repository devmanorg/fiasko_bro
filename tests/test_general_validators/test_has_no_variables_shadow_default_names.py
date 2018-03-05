from fiasko_bro import validators


def test_has_no_variables_shadow_defaults_fail(test_repo):
    output = validators.has_no_variables_that_shadow_default_names(test_repo)
    assert isinstance(output, tuple)
    assert output[0] == 'title_shadows'


def test_has_no_variables_shadow_defaults_ok(origin_repo):
    output = validators.has_no_variables_that_shadow_default_names(origin_repo)
    assert output is None
