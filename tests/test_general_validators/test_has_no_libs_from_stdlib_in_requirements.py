from fiasko_bro.validators import has_libs_from_stdlib_in_requirements


def test_has_libs_from_stdlib_in_requirements_fails(origin_repo):
    expected_output = 'collections==2.0.0, sys==2.0.0'
    output = has_libs_from_stdlib_in_requirements(origin_repo)
    assert output == expected_output


def test_has_libs_from_stdlib_in_requirements_succeeds(test_repo):
    output = has_libs_from_stdlib_in_requirements(test_repo)
    assert output is None
