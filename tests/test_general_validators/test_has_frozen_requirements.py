from fiasko_bro import validators


def test_has_frozen_requirements_no_frozen(test_repo):
    expected_output = 'unfrozen_requirements', 'например, django'
    output = validators.has_frozen_requirements(
        solution_repo=test_repo,
    )
    assert output == expected_output


def test_has_frozen_requirements_no_requirements_file(origin_repo):
    output = validators.has_frozen_requirements(
        solution_repo=origin_repo,
    )
    assert output is None
